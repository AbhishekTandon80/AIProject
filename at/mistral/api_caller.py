import os
from mistralai import Mistral
from dotenv import load_dotenv
from time import sleep
import functools
import json
from at.mongo.mongo_util import DBCall

class MistralCaller:
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
                            "description": "Name of person.",
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
                            "description": "Name of person.",
                        }
                    },
                    "required": ["name"],
                },
            },
        }
    ]

    def __init__(self):
        load_dotenv()
        self.api_key = os.environ["MISTRAL_API_KEY"]
        self.model = "mistral-large-latest"
        self.db_call = DBCall()
        self.names_to_functions = {
            'return_address_for_given_name': self.return_address_for_given_name,
            'return_id_for_given_name': self.return_id_for_given_name
        }

    def return_address_for_given_name(self, name):
        return self.db_call.fetch_address_for_name(name).address

    def return_id_for_given_name(self, name):
        return self.db_call.fetch_id_for_name(name).Id

    def response_from_mistral(self, messages):
        client = Mistral(api_key=self.api_key)
        response = client.chat.complete(
            model=self.model,
            messages=messages,
            tools=self.tools,
            tool_choice="auto",
        )
        resp = response.choices[0].message

        if resp.tool_calls is None:
            return response

        messages.append(resp)
        for tool_call in resp.tool_calls:
            function_name = tool_call.function.name
            function_params = json.loads(tool_call.function.arguments)
            print(f"\nfunction_name: {function_name}\nfunction_params: {function_params}")
            function_result = self.names_to_functions[function_name](**function_params)
            messages.append({
                "role": "tool",
                "name": function_name,
                "content": function_result,
                "tool_call_id": tool_call.id
            })

        sleep(2)
        return client.chat.complete(
            model=self.model,
            messages=messages
        )
