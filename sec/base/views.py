from django.shortcuts import render
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
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

def home(request):
    q=request.GET.get('q') 
    if request.GET.get('q')!=None:
        comp=db.find_one({'ticker':q})
        if comp==None:
            return render(request, 'base/static.html')
        context={'comp':comp,'compid':comp['_id']}
        return render(request, 'base/home.html',context)
    return render(request, 'base/static.html')

def comp(request,pk):
    comp=db.find_one(ObjectId(pk))
    context={'comp':comp} 
    return render(request, 'base/comp.html',context)

