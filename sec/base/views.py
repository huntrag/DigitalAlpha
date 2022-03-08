from django.shortcuts import render
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
import pymongo
from dotenv import load_dotenv
import datetime
import os

load_dotenv()
MONGODB_URI = os.environ['MONGODB_URI']

client = pymongo.MongoClient(MONGODB_URI)
db1=client['tech-meet']
db=db1['comp_names']


def home(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    
    comp=db.find_one({'ticker':q})
    print(comp)
    context={'comp':comp}
    return render(request, 'base/home.html',context)

def comp(request,pk):
    comp=db.find_one({'_id':pk})
    context={'comp':comp} 
    return render(request, 'base/comp.html',context)