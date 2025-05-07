import pymongo
from model.CutomerMapping import NameAddressMapping, NameIdMapping

customerInformationDatabase = "customer_info"
nameAddressMappingCollection = "name_address_mapping"
nameIdMappingCollection = "name_id_mapping"

class DBCall:
    def __init__(self):
        self.mongoClient = pymongo.MongoClient("mongodb://localhost:27017/")

    def fetchAddressForName(self, name):
        print("Fetching address from Mongo DB for: " + name)
        col = self.mongoClient[customerInformationDatabase][nameAddressMappingCollection]
        query = {"name": name}
        resp = col.find_one(query)
        o = NameAddressMapping(resp.get("address"), resp.get("address"))
        return o

    def fetchIdForName(self, name):
        print("Fetching id from Mongo DB for: " + name)
        col = self.mongoClient[customerInformationDatabase][nameIdMappingCollection]
        query = {"name": name}
        resp = col.find_one(query)
        o = NameIdMapping(resp.get("address"), resp.get("id"))
        return o
