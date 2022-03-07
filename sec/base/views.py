from django.shortcuts import render
from utils import get_collection
from django.shortcuts import render, redirect
from django.http import HttpRespons
# Create your views here.

def home(request):
    return render(request, 'base/home.html')

def comp(request,pk):
    db=get_collection('comp-names')
    comp=db.find_one({'_id':pk})
    context={'comp':comp}
    return render(request, 'base/room.html', context)