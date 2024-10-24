from asyncio import sleep
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
import boto3
import botocore
from botocore.config import Config
import json
import uuid
import os
from bedrock_agent_runtime_wrapper import BedrockAgentRuntimeWrapper

load_dotenv()
session = boto3.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name="us-east-1"    
)
bedrock_config = Config(connect_timeout=120, read_timeout=120, retries={'max_attempts': 0})
bedrock_client = session.client('bedrock-runtime', region_name="us-east-1", config=bedrock_config)
bedrock_agent_client = boto3.client("bedrock-agent-runtime", 
                                   config=bedrock_config, region_name="us-east-1")
client = BedrockAgentRuntimeWrapper(bedrock_client)
session_id = str(uuid.uuid4())
kb_id = "Y5Z19MME7R"
app = Flask(__name__)
CORS(app)

chat_history = [ {
            "role": "system",
            "content": f"""You are an assistant to a Valorant esports analyst and you're tasked with providing strategy and tactics around team formation and play style."""
            }, ]
@app.route('/', methods=['POST'])
def hello_world():
    data = request.get_json().get('prompt')
    response = retrieve(data, kb_id, 5)
    contexts = get_contexts(response["retrievalResults"])
    newMessage = {
            "role": "user",
            "content": f"""Use the documents given to you within the context tags to provide basis in your answers to the question in the question tags. Be concise with your answers <context>{contexts}</context> <question>{data}</question>"""
            }
    body = json.dumps({
        "messages": chat_history + [newMessage],
        "max_tokens": 1024,
        "temperature": 0.7,
        "top_p": 0.9,
        "stop": ["###"],
        "n": 1
        })
    modelId = "ai21.jamba-1-5-mini-v1:0"  # change this to use a different version from the model provider
    accept = "application/json"
    contentType = "application/json"
    print(body)
    try:
        
        response = bedrock_client.invoke_model(
            body=body, modelId=modelId, accept=accept, contentType=contentType
        )
        response_body = json.loads(response.get("body").read())
        answer = response_body

    except botocore.exceptions.ClientError as error:
        if  error.response['Error']['Code'] == 'AccessDeniedException':
            print(f"\x1b[41m{error.response['Error']['Message']}\
            \nTo troubeshoot this issue please refer to the following resources.\
            \nhttps://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_access-denied.html\
            \nhttps://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html\x1b[0m\n")      
            class StopExecution(ValueError):
                def _render_traceback_(self):
                    pass
            raise StopExecution        
        else:
            raise error
    model_response = answer["choices"][0]["message"]["content"]
    chat_history.append(newMessage)
    chat_history.append({"role": "assistant", "content": model_response})
    return jsonify({'reply': model_response})

def get_contexts(retrievalResults):
    contexts = []
    for retrievedResult in retrievalResults: 
        contexts.append(retrievedResult['content']['text'])
    return contexts

def retrieve(query, kbId, number_of_results = 5):
    return bedrock_agent_client.retrieve(
        retrievalQuery= {
            'text': query
        },
        knowledgeBaseId=kbId,
        retrievalConfiguration = {
            'vectorSearchConfiguration': {
                'numberOfResults': number_of_results,
                'overrideSearchType': "HYBRID"
            }
        }
    )
if __name__ == '__main__':
    app.run()