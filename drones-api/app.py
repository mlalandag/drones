import pymongo
from flask import Flask, request, jsonify
import os

MONGO_DB_URI=os.environ.get("MONGO_DB_URI")
KAFKA_BOOSTRAP_SERVERS=os.environ.get("KAFKA_BOOSTRAP_SERVERS")

client = pymongo.MongoClient(MONGO_DB_URI, tlsAllowInvalidCertificates=True)
db = client.cabifly

app = Flask(__name__)

@app.route("/drones", methods=["GET"])
def get_cart():
    
    lon = float(request.args.get("lon", -3.7038))
    lat = float(request.args.get("lat", 40.4168))
    distance = float(request.args.get("distance", 100000))

    items = list(db.drones.find(
        {
            "location": {
                 "$near": {
                   "$geometry": {
                      "type": "Point" ,
                      "coordinates": (lon, lat)
                   },
                   "$maxDistance": distance,
                   "$minDistance": 0
                 }
               }
        },
        {"_id": 0}
    ))
    
    return jsonify(items)
