"""Parse the following dataset : https://public.opendatasoft.com/explore/dataset/vehicules-commercialises/download
/?format=json&timezone=Europe/Berlin&lang=fr"""

from pymongo import MongoClient
from json import loads

db = MongoClient("127.0.0.1").mazout.co2Data
with open("../data/vehicules-commercialises.json", 'r') as f:
    json_content = f.read()

co2_data = loads(json_content)
i = 0

for element in co2_data:
    db.insert(element["fields"])
    i += 1
    print(f"Inserted {i} elements into database.")
