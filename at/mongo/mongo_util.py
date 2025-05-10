import pymongo
from at.model.CutomerMapping import NameAddressMapping, NameIdMapping

customer_information_database = "customer_info"
name_address_mapping_collection = "name_address_mapping"
name_id_mapping_collection = "name_id_mapping"

class DBCall:
    def __init__(self):
        self.mongoClient = pymongo.MongoClient("mongodb://localhost:27017/")

    def fetch_address_for_name(self, name):
        print("Fetching address from Mongo DB for: " + name)
        col = self.mongoClient[customer_information_database][name_address_mapping_collection]
        query = {"name": name}
        resp = col.find_one(query)
        o = NameAddressMapping(resp.get("address"), resp.get("address"))
        return o

    def fetch_id_for_name(self, name):
        print("Fetching id from Mongo DB for: " + name)
        col = self.mongoClient[customer_information_database][name_id_mapping_collection]
        query = {"name": name}
        resp = col.find_one(query)
        o = NameIdMapping(resp.get("address"), resp.get("id"))
        return o
