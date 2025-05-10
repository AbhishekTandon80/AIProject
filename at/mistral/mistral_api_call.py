import os
from mistralai import Mistral
from dotenv import load_dotenv
import functools
from time import sleep
import json

load_dotenv()  # take environment variables
api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"

from at.mongo.mongo_util import DBCall
dbCall = DBCall()

def return_address_for_given_name(name):
    ret = dbCall.fetch_address_for_name(name)
    return ret.address

def return_id_for_given_name(name):
    ret = dbCall.fetch_id_for_name(name)
    return ret.Id


tools = [
    {
        "type": "function",
        "function": {
            "name": "return_address_for_given_name",
            "description": "Get address for a name",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "name of person.",
                    }
                },
                "required": ["name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "return_id_for_given_name",
            "description": "Get Id for a name",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Id of person.",
                    }
                },
                "required": ["name"],
            },
        },
    }
]



names_to_functions = {
  'return_address_for_given_name': return_address_for_given_name,
  'return_id_for_given_name': return_id_for_given_name
}

messages = [{"role": "user", "content": "What is address if Hannah?"}]

client = Mistral(api_key=api_key)
response = client.chat.complete(
    model = model,
    messages = messages,
    tools = tools,
    tool_choice = "auto",
)
resp = response.choices[0].message

messages.append(response.choices[0].message)

if (resp.tool_calls == None):
    print("Final output >>  " + response.choices[0].message.content)
else:
    for tool_call in resp.tool_calls:
        function_name = tool_call.function.name
        function_params = json.loads(tool_call.function.arguments)
        print("\nfunction_name: ", function_name, "\nfunction_params: ", function_params)
        function_result = names_to_functions[function_name](**function_params)
        messages.append({"role": "tool", "name": function_name, "content": function_result, "tool_call_id": tool_call.id})

    sleep(2)
    response = client.chat.complete(
        model = model,
        messages = messages
    )
    print("Final output >>  "+ response.choices[0].message.content)

