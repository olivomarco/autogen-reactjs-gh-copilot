# Create ReactJS code from HTML code using custom components with GH Copilot

This repo demonstrates how to create ReactJS code from HTML code using custom components using a GitHub Copilot extension.

To create an extension:

1) deploy this application ([main.py](/main.py) together with [custom_library_src](/custom_library_src/)) on Azure Container Apps publicly (see section below), and take note of the URL. The application, publically accessible, will verify if the request is coming from a GitHub Copilot extension user
2) create a new [GitHub Apps](https://github.com/settings/apps), under any name of choice. Fill ```homepage URL``` and ```callback URL``` with the URL from step 1; flag ```Request user authorization (OAuth) during installation``` and ```Enable Device Flow```
3) under ```Copilot``` in the GitHub App, fill ```App Type``` with ```Agent```, and fill ```URL``` with the URL from step 1. Add a custom description
4) Install the app on your GitHub account or any organization of choice, from the ```Install App``` menu on the left
5) Under ```Permissions & events```, under ```Account permissions```, give read-only access to Copilot Chat

From now forward, you should be able to see in your Copilot Chat the option to invoke the extension by starting with ```@``` and the name of the app you created in step 2.
Pass it some HTML code as command or highlight some HTML code and invoke the extension (for example: ```@reactjs-from-html <html code>``` or ```@reactjs-from-html #selection```).

## Deploying the application to Azure Container Apps

First, you have to create an ```OAI_CONFIG_LIST``` file in the main directory with your details.

**NOTE/DISCLAIMER**: this is bad practice, since the secret file will be embeded in the container image. This is just for demonstration purposes.

If you want to deploy the application to Azure Container Apps, you can use the following script as a starting point:

```bash
# Variables
RESOURCE_GROUP=myResourceGroup
LOCATION=eastus
ACR_NAME=mycontainerregistry$(openssl rand -hex 5)
ENV_NAME=mycontainerapp-env
IMAGE_NAME=myapp$(uuidgen | tr -d '-')
APP_NAME=mycontainerapp$(openssl rand -hex 5)

# Step 1: Create Resource Group
echo "Creating resource group..."
az group create --name $RESOURCE_GROUP --location $LOCATION

# Step 2: Create Azure Container Registry
echo "Creating Azure Container Registry..."
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic --admin-enabled true
ACR_LOGIN_SERVER=$(az acr show --name $ACR_NAME --resource-group $RESOURCE_GROUP --query loginServer --output tsv)

# Step 3: Log in to ACR
echo "Logging into ACR..."
az acr login --name $ACR_NAME

# Step 4: Build Docker Image
echo "Building Docker image..."
cd path/to/my_app
docker build -t $ACR_LOGIN_SERVER/$IMAGE_NAME:latest .

# Step 5: Push Docker Image to ACR
echo "Pushing Docker image to ACR..."
docker push $ACR_LOGIN_SERVER/$IMAGE_NAME:latest

# Step 6: Create Container App Environment
echo "Creating Container App Environment..."
az containerapp env create --name $ENV_NAME --resource-group $RESOURCE_GROUP --location $LOCATION

# Step 7: Deploy Container App
echo "Deploying Container App..."
az containerapp create \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --environment $ENV_NAME \
  --image $ACR_LOGIN_SERVER/$IMAGE_NAME:latest \
  --target-port 8000 \
  --ingress 'external' \
  --cpu 0.5 \
  --memory 1.0Gi \
  --min-replicas 1 \
  --max-replicas 5 \
  --environment-variables APP_MODE=production DATABASE_URL=postgres://user:password@dbserver:5432/mydb

# Step 8: Assign ACR Pull Permissions
echo "Assigning ACR pull permissions..."
az containerapp identity assign --name $APP_NAME --resource-group $RESOURCE_GROUP
IDENTITY_CLIENT_ID=$(az containerapp show --name $APP_NAME --resource-group $RESOURCE_GROUP --query identity.principalId --output tsv)
ACR_ID=$(az acr show --name $ACR_NAME --resource-group $RESOURCE_GROUP --query id --output tsv)
az role assignment create --assignee $IDENTITY_CLIENT_ID --role acrpull --scope $ACR_ID

# Encode the oai_config_list file content
OAI_CONFIG_CONTENT=$(base64 < OAI_CONFIG_LIST)

# Add the secret to the Container App
az containerapp secret set \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --secrets OAI_CONFIG_LIST=$OAI_CONFIG_CONTENT

az containerapp update \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --environment-variables OAI_CONFIG_LIST=secretref:OAI_CONFIG_LIST

# Step 9: Retrieve and Display App URL
FQDN=$(az containerapp show --name $APP_NAME --resource-group $RESOURCE_GROUP --query properties.configuration.ingress.fqdn --output tsv)
echo "Your Container App is running at: http://$FQDN"
```
