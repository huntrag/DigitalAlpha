import asyncio
from django.shortcuts import render
from . import utils
import pandas as pd
import sys
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
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

db1 = client['tech-meet']
db_only=db1['comp']
db= db1['info']

db_form = db1['form-data']


def parse_json(data):
    return json.loads(json_util.dumps(data))


def getAll(request):
    try:
        q = request.GET.get('q')
        if q.isdigit():
            data = db.find({'cik': int(q)})
        else:
            data = db.find({'$or': [
                {'ticker': {'$regex': f'^{q}'}},
                {'title': {'$regex': f'^{q}'}},
            ]})
        return JsonResponse(parse_json({'status': 'success', 'data': data}),status=200)
    except:
        return JsonResponse(parse_json({'status': 'fail'}),status=404)


def getStrict(request):
    try:
        q = request.GET.get('q')
        print(q)
        if q.isdigit():
            data = db.find_one({'cik': int(q)})
        else:
            data = db.find_one({'ticker': q})
        return JsonResponse(parse_json({'status': 'success', 'data': data}),status=200)
    except:
        return JsonResponse(parse_json({'status': 'fail'}),status=404)


def getBS(request):
    try:
        q1=request.GET.get('q1')
        q2=request.GET.get('q2')
        print(q1,q2)
        # print(raw['ticker'])
        # data=raw['data']

        
        # ans=[]

        # for r in db:
        #     d=r['data']
        #     d['date']=r['date']
        #     year=r['date'].split('-')[0]
        #     d['year']=year
        #     ans.append(d)
        CDK=(utils.generateDF(int(q1),2,str(q2),"2023-00-00"))
        newfile = pd.DataFrame.from_dict(CDK)
        
        ans=utils.convertToJson(newfile)

        # data = db_form.find({'ticker': raw['ticker']})
        return JsonResponse(parse_json({'status': 'success', 'data': ans}),status=200)
    except:
        return JsonResponse(parse_json({'status': 'fail'}),status=404)

#request body of form
# {
#     "date":"2017-01-01",
#     "cik":796343 
# }

def getId(request, pk):
    try:
        data = db.find_one({"_id": ObjectId(pk)})
        return JsonResponse(parse_json({'status': 'success', 'data': data}),status=200)
    except:
        return JsonResponse(parse_json({'status': 'failll'}),status=404)


def comp(request):
    try:
        t1=str(request.GET.get('t1'))
        t2=str(request.GET.get('t2'))
        print(t1)
        print(t2)
        data = list(db_form.find({'$and':[{{'$or': [
                {'ticker': t1},
                {'ticker': t2}
            ]},
            {'$gte':{'date':'2021-11-21'}}
            }]}
        ))
        print(data)
        return JsonResponse(parse_json({'status': 'success'}),status=200)
    except:
        return JsonResponse(parse_json({'status': 'fail'}),status=404)   
