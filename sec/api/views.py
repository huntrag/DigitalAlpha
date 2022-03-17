import asyncio
from django.shortcuts import render
from . import utils
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
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
print(client)
db1 = client['tech-meet']
db = db1['comp']
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
        return JsonResponse(parse_json({'status': 'success', 'data': data}))
    except:
        return JsonResponse(parse_json({'status': 'fail'}))


def getStrict(request):
    try:
        q = request.GET.get('q')
        print(q)
        if q.isdigit():
            data = db.find_one({'cik': int(q)})
        else:
            data = db.find_one({'ticker': q})
        return JsonResponse(parse_json({'status': 'success', 'data': data}))
    except:
        return JsonResponse(parse_json({'status': 'fail'}))


def getBS(request):
    try:
        raw = json.loads(request.body)
        # print(raw['ticker'])
        # data=raw['data']
        data = db_form.find(
            {'date': {"$gte": raw['date']}, 'ticker': raw['ticker']})
        # data = db_form.find({'ticker': raw['ticker']})
        return JsonResponse(parse_json({'status': 'success', 'data': data}))
    except:
        return JsonResponse(parse_json({'status': 'fail'}))


def getId(request, pk):
    try:
        data = db.find_one({"_id": ObjectId(pk)})
        id = ObjectId(pk)
        print(id)
        print(data)
        cik = data['cik']
        text = utils.getSummary(cik)
        print(text)
        return JsonResponse(parse_json({'status': 'success', 'data': data, 'text': text}))
    except:
        return JsonResponse(parse_json({'status': 'fail'}))
