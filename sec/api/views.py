from django.shortcuts import render
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import pymongo
from dotenv import load_dotenv
import datetime
import os
import json
from bson.objectid import ObjectId
from bson import BSON
from bson import json_util 
load_dotenv()
MONGODB_URI = os.environ['MONGODB_URI']

client = pymongo.MongoClient(MONGODB_URI)
db1=client['tech-meet']
db=db1['comp_names']
db2=client['test']['datem']

def parse_json(data):
    return json.loads(json_util.dumps(data))

def getAll(request):
    try:
        q=request.GET.get('q')
        print(q)
        data=db.find({'$or':[
            {'ticker':{'$regex':f'^{q}'}},
            {'cik':int(q)},
            {'title':{'$regex':f'^{q}'}}
            ]})
        return JsonResponse(parse_json({'status':'success','data':data}))
    except:
        return JsonResponse(parse_json({'status':'fail'}))

def getStrict(request):
    try:
        q=request.GET.get('q')
        data=db.find({'$or':[
            {'ticker':q},
            {'cik':int(q)},
            {'title':q}
            ]})
        return JsonResponse(parse_json({'status':'success','data':data}))
    except:
        return JsonResponse(parse_json({'status':'fail'}))


def getId(request,pk):
    try:
        print(pk)
        data=db.find_one(ObjectId(pk))
        return JsonResponse(parse_json({'status':'success','data':data}))
    except:
        return JsonResponse(parse_json({'status':'fail'}))
