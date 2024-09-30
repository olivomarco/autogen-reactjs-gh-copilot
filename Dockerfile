# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set environment variables to prevent Python from buffering and writing bytecode
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy custom libraries
COPY custom_library_src/ ./custom_library_src/

# Copy the rest of the application code
COPY main.py .

# (Optional) Expose a port if your app runs a server, e.g., 8000
EXPOSE 8000

# Define the command to run the application
CMD ["python", "main.py"]
