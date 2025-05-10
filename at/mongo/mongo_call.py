import pymongo

mongoClient = pymongo.MongoClient("mongodb://localhost:27017/")

customer_information_database = "customer_info"
name_address_mapping_collection = "name_address_mapping"


customerdb = mongoClient[customer_information_database]
name_address_mapping_col = customerdb[name_address_mapping_collection]

nameAddressMapping = [
  { "name": "Amy", "address": "Apple st 652"},
  { "name": "Hannah", "address": "Mountain 21"},
  { "name": "Michael", "address": "Valley 345"},
  { "name": "Sandy", "address": "Ocean blvd 2"},
  { "name": "Betty", "address": "Green Grass 1"},
  { "name": "Richard", "address": "Sky st 331"},
  { "name": "Susan", "address": "One way 98"},
  { "name": "Vicky", "address": "Yellow Garden 2"},
  { "name": "Ben", "address": "Park Lane 38"},
  { "name": "William", "address": "Central st 954"},
  { "name": "Chuck", "address": "Main Road 989"},
  { "name": "Viola", "address": "Sideway 1633"}
]

x = name_address_mapping_col.insert_many(nameAddressMapping)


nameIdMapping = [
    { "name": "Amy", "id": "id1233"},
    { "name": "Hannah", "id": "id1234"},
    { "name": "Michael", "id": "id1235"},
    { "name": "Sandy", "id": "1236"},
    { "name": "Betty", "id": "1237"},
    { "name": "Richard", "id": "1238"}
]

# customerInformationDatabase = "customer_info"
name_id_mapping_collection = "name_id_mapping"
name_id_mapping_col = customerdb[name_id_mapping_collection]

y = name_id_mapping_col.insert_many(nameIdMapping)
