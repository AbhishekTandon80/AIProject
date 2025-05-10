from at.mistral.ApiCaller import MistralCaller
content = "What's the Id of person Amy?"
apiCaller = MistralCaller()

resp = apiCaller.response_from_mistral(content)
print("response from mistal ai >> " + resp)