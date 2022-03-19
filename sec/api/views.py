from . import utils
import pandas as pd
import json
from django.http import JsonResponse
import pymongo
from dotenv import load_dotenv
import os
import json
from bson.objectid import ObjectId
from bson import json_util
load_dotenv()
MONGODB_URI = os.environ['MONGODB_URI']

client = pymongo.MongoClient(MONGODB_URI)

collection = client['tech-meet']

db_info= collection['info']
db_form = collection['form-data']
db_stock=collection['stock']

def parse_json(data):
    return json.loads(json_util.dumps(data))

def getAll(request):
    try:
        q = request.GET.get('q')
        if q.isdigit():
            data = db_info.find({'cik': int(q)})
        else:
            data = db_info.find({'$or': [
                {'ticker': {'$regex': f'^{q}'}},
                {'title': {'$regex': f'^{q}'}},
            ]})
        return JsonResponse(parse_json({'status': 'success', 'data': data}),status=200)
    except:
        return JsonResponse(parse_json({'status': 'fail'}),status=404)

def getStrict(request):
    try:
        q = request.GET.get('q')
        if q.isdigit():
            data = db_info.find_one({'cik': int(q)})
        else:
            data = db_info.find_one({'ticker': q})
        return JsonResponse(parse_json({'status': 'success', 'data': data}),status=200)
    except:
        return JsonResponse(parse_json({'status': 'fail'}),status=404)

def getStock(request):
    try:
        q=request.GET.get('q')

        data=db_stock.find_one({'Ticker':str(q)})
        return JsonResponse(parse_json({'status': 'success', 'data': data}),status=200)
    except:
         return JsonResponse(parse_json({'status': 'fail'}),status=404)


def getBS(request):
    try:
        q1=request.GET.get('q1')
        q2=request.GET.get('q2')

        CDK=(utils.generateDF(int(q1),2,str(q2),"2023-00-00"))
        newfile = pd.DataFrame.from_dict(CDK)
        
        ans=utils.convertToJson(newfile)
        return JsonResponse(parse_json({'status': 'success', 'data': ans}),status=200)
    except:
        return JsonResponse(parse_json({'status': 'fail'}),status=404)

def getId(request, pk):
    try:
        data = db_info.find_one({"_id": ObjectId(pk)})
        return JsonResponse(parse_json({'status': 'success', 'data': data}),status=200)
    except:
        return JsonResponse(parse_json({'status': 'fail'}),status=404)

    
