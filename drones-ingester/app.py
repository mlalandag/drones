from kafka import KafkaConsumer
import pymongo
import json
import os

MONGO_DB_URI=os.environ.get("MONGO_DB_URI")
KAFKA_BOOSTRAP_SERVERS=os.environ.get("KAFKA_BOOSTRAP_SERVERS")

client = pymongo.MongoClient(MONGO_DB_URI, tlsAllowInvalidCertificates=True)
db = client.cabifly

consumer = KafkaConsumer(
    'cabifly.drones',
     bootstrap_servers=[KAFKA_BOOSTRAP_SERVERS],
     auto_offset_reset='earliest'
)

for message in consumer:
    item = json.loads(message.value)["data"]
    
    db.drones.update_one(
        {"drone_id": item["drone_id"]},
        {"$set": {"location": item["location"]}},
        upsert = True
    )