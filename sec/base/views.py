from django.shortcuts import render
from . import utils
from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request, 'base/home.html')

def comp(request,pk):
    db=utils.get_collection('comp-names')
    comp=db.find_one({'_id':pk})
    context={'comp':comp}
    return render(request, 'base/room.html', context)