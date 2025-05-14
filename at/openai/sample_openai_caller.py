from dotenv import load_dotenv
from at.openai.ApiCaller import OpenAICaller

load_dotenv()
function_caller = OpenAICaller()
message = "what is the address and Id of Hannah?"
input_messages = [{"role": "user", "content": message}]
function_caller.get_response_from_openai(input_messages)
