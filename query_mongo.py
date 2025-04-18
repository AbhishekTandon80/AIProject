import pymongo

from CutomerMapping import NameAddressMapping

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

customerInformationDatabase = "customer_info"
nameAddressMappingCollection = "name_address_mapping"

db = myclient[customerInformationDatabase]
col = db[nameAddressMappingCollection]

myquery = { "address": "Park Lane 38" }



doc = col.find(myquery)

for x in doc:
  resp = (NameAddressMapping(x.get("name"), x.get("address")))
  print("Name >> " + resp.name + " ; Address >> " + resp.address)