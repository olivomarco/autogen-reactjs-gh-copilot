import autogen
import os, sys
import glob
from autogen import register_function
from flask import Flask, request, Response
import time
import json
from pydantic import BaseModel
from typing import Union, Optional
from verify_signatures import verify_request_by_key_id

###########################
# SAMPLE CODE
###########################
html_code = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="/docs/4.0/assets/img/favicons/favicon.ico">

    <title>Pricing example - Bootstrap</title>

    <link rel="canonical" href="https://getbootstrap.com/docs/4.0/examples/pricing/">

    <!-- Bootstrap core CSS -->
    <link href="../../dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="pricing.css" rel="stylesheet">
  </head>

  <body>

    <div class="d-flex flex-column flex-md-row align-items-center p-3 px-md-4 mb-3 bg-white border-bottom box-shadow">
      <h5 class="my-0 mr-md-auto font-weight-normal">Company name</h5>
      <nav class="my-2 my-md-0 mr-md-3">
        <a class="p-2 text-dark" href="#">Features</a>
        <a class="p-2 text-dark" href="#">Enterprise</a>
        <a class="p-2 text-dark" href="#">Support</a>
        <a class="p-2 text-dark" href="#">Pricing</a>
      </nav>
      <a class="btn btn-outline-primary" href="#">Sign up</a>
    </div>

    <div class="pricing-header px-3 py-3 pt-md-5 pb-md-4 mx-auto text-center">
      <h1 class="display-4">Pricing</h1>
      <p class="lead">Quickly build an effective pricing table for your potential customers with this Bootstrap example. It's built with default Bootstrap components and utilities with little customization.</p>
    </div>

    <div class="container">
      <div class="card-deck mb-3 text-center">
        <div class="card mb-4 box-shadow">
          <div class="card-header">
            <h4 class="my-0 font-weight-normal">Free</h4>
          </div>
          <div class="card-body">
            <h1 class="card-title pricing-card-title">$0 <small class="text-muted">/ mo</small></h1>
            <ul class="list-unstyled mt-3 mb-4">
              <li>10 users included</li>
              <li>2 GB of storage</li>
              <li>Email support</li>
              <li>Help center access</li>
            </ul>
            <button type="button" class="btn btn-lg btn-block btn-outline-primary">Sign up for free</button>
          </div>
        </div>
        <div class="card mb-4 box-shadow">
          <div class="card-header">
            <h4 class="my-0 font-weight-normal">Pro</h4>
          </div>
          <div class="card-body">
            <h1 class="card-title pricing-card-title">$15 <small class="text-muted">/ mo</small></h1>
            <ul class="list-unstyled mt-3 mb-4">
              <li>20 users included</li>
              <li>10 GB of storage</li>
              <li>Priority email support</li>
              <li>Help center access</li>
            </ul>
            <button type="button" class="btn btn-lg btn-block btn-primary">Get started now</button>
          </div>
        </div>
        <div class="card mb-4 box-shadow">
          <div class="card-header">
            <h4 class="my-0 font-weight-normal">Enterprise</h4>
          </div>
          <div class="card-body">
            <h1 class="card-title pricing-card-title">$29 <small class="text-muted">/ mo</small></h1>
            <ul class="list-unstyled mt-3 mb-4">
              <li>30 users included</li>
              <li>15 GB of storage</li>
              <li>Phone and email support</li>
              <li>Help center access</li>
            </ul>
            <button type="button" class="btn btn-lg btn-block btn-primary">Contact us</button>
          </div>
        </div>
      </div>

      <footer class="pt-4 my-md-5 pt-md-5 border-top">
        <div class="row">
          <div class="col-12 col-md">
            <img class="mb-2" src="https://getbootstrap.com/docs/4.0/assets/brand/bootstrap-solid.svg" alt="" width="24" height="24">
            <small class="d-block mb-3 text-muted">&copy; 2017-2018</small>
          </div>
          <div class="col-6 col-md">
            <h5>Features</h5>
            <ul class="list-unstyled text-small">
              <li><a class="text-muted" href="#">Cool stuff</a></li>
              <li><a class="text-muted" href="#">Random feature</a></li>
              <li><a class="text-muted" href="#">Team feature</a></li>
              <li><a class="text-muted" href="#">Stuff for developers</a></li>
              <li><a class="text-muted" href="#">Another one</a></li>
              <li><a class="text-muted" href="#">Last time</a></li>
            </ul>
          </div>
          <div class="col-6 col-md">
            <h5>Resources</h5>
            <ul class="list-unstyled text-small">
              <li><a class="text-muted" href="#">Resource</a></li>
              <li><a class="text-muted" href="#">Resource name</a></li>
              <li><a class="text-muted" href="#">Another resource</a></li>
              <li><a class="text-muted" href="#">Final resource</a></li>
            </ul>
          </div>
          <div class="col-6 col-md">
            <h5>About</h5>
            <ul class="list-unstyled text-small">
              <li><a class="text-muted" href="#">Team</a></li>
              <li><a class="text-muted" href="#">Locations</a></li>
              <li><a class="text-muted" href="#">Privacy</a></li>
              <li><a class="text-muted" href="#">Terms</a></li>
            </ul>
          </div>
        </div>
      </footer>
    </div>


    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script>window.jQuery || document.write('<script src="../../assets/js/vendor/jquery-slim.min.js"><\/script>')</script>
    <script src="../../assets/js/vendor/popper.min.js"></script>
    <script src="../../dist/js/bootstrap.min.js"></script>
    <script src="../../assets/js/vendor/holder.min.js"></script>
    <script>
      Holder.addTheme('thumb', {
        bg: '#55595c',
        fg: '#eceeef',
        text: 'Thumbnail'
      });
    </script>
  </body>
</html>
"""

###########################
# GLOBAL VARIABLES
###########################
BASE_FOLDER = "custom_library_src"

endObject = {
    "choices": [{ "index": 0, "finish_reason": "stop", "delta": { "content": None } }]
}

###########################
# DEFINE METHODS TO GENERATE RESPONSE
###########################
def generate(llm_response):
    #for word in llm_response.split():
        #yield f'data: {{"choices": [{{ "index": 0, "delta": {{ "content": {json.dumps(word)}, "role": "assistant" }} }}]}}\n\n'
        #time.sleep(0.1)
    yield f'data: {{"choices": [{{ "index": 0, "delta": {{ "content": {json.dumps(llm_response)}, "role": "assistant" }} }}]}}\n\n'
    yield f"data: {json.dumps(endObject)}\n\ndata: [DONE]\n\n"


# Capture the last message from response_writer_assistant before TERMINATE
def get_final_response_writer_message(messages):
    for message in reversed(messages):
        # Check if the message is from
        if message.get("name", "") == "response_writer_assistant":
            # if message is only TERMINATE, check the previous message
            if message.get("content", "").strip() == "TERMINATE":
                continue
            # remove "TERMINATE" from the message and return it
            return message.get("content", "").replace("TERMINATE", "").strip()
    return None


###########################
# DEFINE THE TOOLS
###########################
class ReactComponentList(BaseModel):
    components: list[str]

def get_react_components_list() -> Union[str, ReactComponentList]:
    # retrieve list of all reactjs components
    files = glob.glob(f"{BASE_FOLDER}/*")
    # remove the path from the file name
    files = [os.path.basename(f) for f in files]

    print(f"Getting React components list: {files}")
    return files


def get_react_component(component_name: str) -> Optional[str]:
    # retrieve code for the given ReactJS component
    print(f"Getting React component: {component_name}")
    if not os.path.exists(f"{BASE_FOLDER}/{component_name}/{component_name}.js"):
        return None

    with open(f"{BASE_FOLDER}/{component_name}/{component_name}.js", "r") as file:
        return file.read()

###########################
# FLASK APP
###########################
def create_app():
    app = Flask(__name__)

    @app.route('/', methods=['POST'])
    def copilot_generate():
        # verify signatures
        raw_body = request.data.decode()
        signature = request.headers.get("Github-Public-Key-Signature", "")
        key_id = request.headers.get("Github-Public-Key-Identifier", "")
        token = request.headers.get("X-Github-Token", "")

        try:
            is_valid = verify_request_by_key_id(raw_body, signature, key_id, token)
            if is_valid:
                print("Request is valid.")
            else:
                return Response("Request is invalid.")
        except Exception as e:
            print(f"Error: {e}")
            return Response(f"Error: {e}.")

        data = json.loads(request.data)
        if data['messages'][-1]['content'] is not None and data['messages'][-1]['content'] != "":
            copilot_content = data['messages'][-1]['content']
        elif data['messages'][-1]['copilot_references'] is None or data not in data['messages'][-1]['copilot_references']:
            #return Response(generate("Please pass **some** input HTML code.\n\n\t/*pricing*/\t\n.princing \{\}\n\n\t<html><body>\n\t<p>echo \"hello <b>world</b>\"</p>\n\t</body>\n\t</html>\n"), mimetype='text/event-stream')
            return Response(generate("Please pass some input HTML code."), mimetype='text/event-stream')
        else:
            copilot_content = data['messages'][-1]['copilot_references'][0]['data']['content']

        user.initiate_chat(
            manager,
            message="Create a new ReactJS component that renders the HTML code provided below.\nHTML code:\n\n" + copilot_content, #html_code,
            summary_method="last_msg"
        )

        # get final message from code_writer_assistant
        final_response_writer_message = get_final_response_writer_message(groupchat.messages)
        return Response(generate(final_response_writer_message), mimetype='text/event-stream')

    return app

###########################
# MAIN CODE
###########################
if __name__ == "__main__":
  config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST")
  llm_config = {"config_list": config_list}

  code_writer_assistant = autogen.ConversableAgent(
      name="code_writer_assistant",
      llm_config=llm_config,
      system_message="You are an assistant that analyzes HTML code and creates a new ReactJS app that renders the HTML code."
                      "First, call get_react_components_list() to get the list of all custom ReactJS components you are allowed to use that are provided by the 'custom_abc' ReactJS components library."
                      "Then, call get_react_component(component_name) to get the code for a specific component you want to use to analyze it, and see if it is the right component to use in your context."
                      "Finally, output the code for the new ReactJS app you created using these components, along with CSS if needed. Format in Markdown format with code (HTML, CSS, JSX, others) that is idented with a tab."
                      "Reply \"TERMINATE\" in the end when everything is done."
  )

  code_reviewer_assistant = autogen.ConversableAgent(
      name="code_reviewer_assistant",
      llm_config=llm_config,
      system_message="You are an assistant that reviews the code written by the code_writer_assistant."
                      "You should analyze the code and provide feedback to the assistant on how to improve it. Remember that the provided 'custom_abc' library must be used by the code writer assistant for the components."
                      "Make sure components included by code_writer_assistant are not hallucinated."
                      "You can also suggest changes to the code if necessary, taking in consideration that the output ReactJS code (and CSS if provided) must render exactly as the input HTML code."
                      "Only reply 'TERMINATE' if the code that the code_writer_assistant provides is fully satisfactory after your feedback and corrections have been implemented."
  )

  response_writer_assistant = autogen.ConversableAgent(
      name="response_writer_assistant",
      llm_config=llm_config,
      system_message="Develop a response using code provided by code_writer_assistant once it has been reviewed and approved by code_reviewer_assistant. Your response will go in a chat with a user."
                      "Do not address the user directly. Start naturally, and do not show that you are a bot. Do not respond with input code again, just with output code that "
                      "the user needs to develop the React component and with instructions. Format in Markdown format with code (HTML, CSS, JSX, others) that is idented with a tab."
                      "Reply \"TERMINATE\" in the end when everything is done."
  )

  register_function(
      get_react_components_list,
      caller=code_writer_assistant,  # The assistant agent can suggest calls to the calculator.
      executor=code_writer_assistant,  # The user proxy agent can execute the calculator calls.
      name="get_react_components_list",  # By default, the function name is used as the tool name.
      description="Get the list of custom ReactJS components",  # A description of the tool.
  )

  register_function(
      get_react_component,
      caller=code_writer_assistant,  # The assistant agent can suggest calls to the calculator.
      executor=code_writer_assistant,  # The user proxy agent can execute the calculator calls.
      name="get_react_component",  # By default, the function name is used as the tool name.
      description="Get the JS contents of a given ReactJS component you need to investigate",  # A description of the tool.
  )

  user = autogen.UserProxyAgent(
      name="User",
      human_input_mode="NEVER",
      is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
      code_execution_config=False,
  )

  groupchat = autogen.GroupChat(agents=[user, code_writer_assistant, code_reviewer_assistant, response_writer_assistant], messages=[], max_round=10)
  manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

  app = create_app()
  app.run(debug=True)
