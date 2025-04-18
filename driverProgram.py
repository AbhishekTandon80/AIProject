from mongo_util import DBCall

dbCall = DBCall()
ret = dbCall.fetchAddressForName("Amy")
print(ret.address)