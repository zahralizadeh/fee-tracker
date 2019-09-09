import requests
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def collectdata(request):
    return HttpResponse('Hi...we are going to Store information about the house you want in database!')

