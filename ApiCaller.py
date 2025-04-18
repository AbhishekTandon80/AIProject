import os
from mistralai import Mistral
from dotenv import load_dotenv
import functools
from time import sleep
from mongo_util import DBCall

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



    def __init__(self):
        load_dotenv()  # take environment variables
        self.api_key = os.environ["MISTRAL_API_KEY"]
        self.model = "mistral-large-latest"
        self.dbCall = DBCall()
        self.names_to_functions = {
            'return_address_for_given_name': functools.partial(self.return_address_for_given_name),
            'return_id_for_given_name': functools.partial(self.return_id_for_given_name)
        }

    def return_address_for_given_name(self, name):
        ret = self.dbCall.fetchAddressForName(name)
        return ret.address

    def return_id_for_given_name(self, name):
        ret = self.dbCall.fetchIdForName(name)
        return ret.Id



    def responseFromMistal(self, content):
        messages = [{"role": "user", "content": content}]

        client = Mistral(api_key=self.api_key)
        response = client.chat.complete(
            model=self.model,
            messages=messages,
            tools=self.tools,
            tool_choice="any",
        )
        resp = response.choices[0].message

        import json
        # calls = response.choices[0].messages.tool_calls

        messages.append(response.choices[0].message)

        for tool_call in resp.tool_calls:
            function_name = tool_call.function.name
            function_params = json.loads(tool_call.function.arguments)
            print("\nfunction_name: ", function_name, "\nfunction_params: ", function_params)
            function_result = self.names_to_functions[function_name](**function_params)
            messages.append(
                {"role": "tool", "name": function_name, "content": function_result, "tool_call_id": tool_call.id})

        sleep(2)
        response = client.chat.complete(
            model=self.model,
            messages=messages
        )
        return response.choices[0].message.content
