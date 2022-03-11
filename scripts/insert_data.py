import pymongo,os,json
from dotenv import load_dotenv
from bson import json_util 
load_dotenv()
MONGODB_URI = os.environ['MONGODB_URI']
import asyncio

client = pymongo.MongoClient(MONGODB_URI)
db1=client['tech-meet']
db=db1['comp']

def parse_json(data):
    return json.loads(json_util.dumps(data))

with open('data/output.json','r') as json_file:
    json_file=json.load(json_file)
    db.insert_many(json_file)