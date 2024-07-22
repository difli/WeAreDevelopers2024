import os
import json
from astrapy import DataAPIClient
from dotenv import load_dotenv

load_dotenv()

with open('../vectorize/bicycle_catalog_100.json') as user_file:
  file_contents = user_file.read()

client = DataAPIClient(os.environ["ASTRA_TOKEN"])
database = client.get_database(os.environ["ASTRA_API_ENDPOINT"])
collection = database.get_collection("bicycle_catalog")

bicycles = json.loads(file_contents)
for bicycle in bicycles:
  print(bicycle.get('product_name'))
  while True:
    try:
      collection.update_one(
        {'_id': bicycle.get('id')},
        {'$set': {
          '$vectorize': bicycle.get("product_description"),
          'content': bicycle.get("product_description"),
          'metadata': {"id": bicycle.get("id"), "bicycle_type": bicycle.get("bicycle_type"), "product_name": bicycle.get("product_name"), "price": bicycle.get("price")}
        }},
        upsert=True
      )
    except Exception as ex:
      print(ex)
      print("Retrying...")
      continue
    break