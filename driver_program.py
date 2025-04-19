from ApiCaller import MistralCaller
content = "What's the Id of person Amy?"
apiCaller = MistralCaller()

resp = apiCaller.responseFromMistral(content)
print("response from mistal ai >> " + resp)