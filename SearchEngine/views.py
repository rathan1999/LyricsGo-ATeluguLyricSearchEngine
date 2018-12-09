from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from .Indexing import InvertedIndex
from .QueryHandler import Query
from functools import reduce
# Create your views here.
from .models import *
import os

def homepage(request):
	if(request.method == "POST" and request.POST.get('location', False) != False):
		instance = InvertedIndex()
		instance.createIndex(request.POST['location'])
		instance.saveIndex()
		return render(request, 'search.html', {"message": "Indices Created Successfully!!!"}) 
	else:	
		return render(request, 'search.html')

def results(request):
	if(request.method == "POST" and request.POST.get('query', False) != False):
		instance = Query()
		result = reduce(lambda x, y: x+y, instance.search(request.POST['query']))
		paths = os.listdir(".\static\\IR")
		urls = []
		for i in result:
			urls.append(paths[i])
		return render(request, 'results.html', {'urls':urls, 'query': request.POST['query']})
	else:
		return redirect('homepage')