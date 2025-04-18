from ApiCaller import MistralCaller
content = "What's the Id of person Amy?"
apiCaller = MistralCaller()

resp = apiCaller.responseFromMistal(content)
print("response from mistal ai >> " + resp)