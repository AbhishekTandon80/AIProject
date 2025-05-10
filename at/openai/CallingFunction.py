from openai import OpenAI
from dotenv import load_dotenv
from at.mongo.mongo_util import DBCall
import json

class OpenAICaller:
    tools = [{
        "type": "function",
        "name": "return_address_for_given_name",
        "description": "Get address for a name",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "name of persons"
                }
            },
            "required": [
                "name"
            ],
            "additionalProperties": False
        }
    }, {
        "type": "function",
        "name": "return_id_for_given_name",
        "description": "Get address for a name",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "name of persons"
                }
            },
            "required": [
                "name"
            ],
            "additionalProperties": False
        }
    }]


    def __init__(self):
        self.client = OpenAI()
        # take environment variables
        load_dotenv()
        self.dbCall = DBCall()
        self.names_to_functions = {
            'return_address_for_given_name': self.return_address_for_given_name,
            'return_id_for_given_name': self.return_id_for_given_name
        }

    def return_address_for_given_name(self, name):
        ret = self.dbCall.fetch_address_for_name(name)
        return ret.address

    def return_id_for_given_name(self, name):
        ret = self.dbCall.fetch_id_for_name(name)
        return ret.Id


    def get_response_from_openai(self, input_messages):

        response = self.make_llm_call(input_messages)

        count = 0
        for tool_call in response.output:
            if tool_call.type != "function_call":
                continue

            function_name = tool_call.name
            function_params = json.loads(tool_call.arguments)
            print("\nfunction_name: ", function_name, "\nfunction_params: ", function_params)
            function_result = self.names_to_functions[function_name](**function_params)
            input_messages.append(tool_call)
            input_messages.append({  # append result message
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": str(function_result)
            })
            count += 1

        if count > 0: response = self.make_llm_call(input_messages)

        return response


    def make_llm_call(self, input_messages):
        return self.client.responses.create(
            model="gpt-4.1",
            input=input_messages,
            tools=self.tools,
            tool_choice="auto"
        )