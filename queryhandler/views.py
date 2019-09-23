# -*- coding: utf-8 -*-

import logging
import requests
from django.http import HttpResponse
from django.shortcuts import render
from .models import PropertyPredictResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


logger = logging.getLogger(__name__)

# Create your views here.
@csrf_exempt
def query_price(request):
    this_offertype = request.GET['offertype']
    this_location = request.GET['location']
    this_area = int(request.GET['area'])
    this_rooms = int(request.GET['rooms'])
    this_age = int(request.GET['age']) 
    #TODO: validate user input

    #TODO: search prediction history before start prediction
    #TODO: token provided or something to prevent robots
    prediction =PropertyPredictResponse(location =this_location, offertype=this_offertype, area=this_area,\
        age=this_age, rooms=this_rooms)
    response = prediction.predict()
    prediction.save()
    return response
    
       


@csrf_exempt
def whatisprice(request):
    this_offertype = request.GET['offertype']
    this_location = request.GET['location']
    this_area = int(request.GET['area'])
    this_rooms = int(request.GET['rooms'])
    this_age = int(request.GET['age']) if 'age' in request.GET else None
    #TODO: validate user input
    data = PropertyFile.objects.filter(offertype=this_offertype,location__contains=this_location,area=this_area,rooms=this_rooms)
    #location__contains=this_location,,area=this_area,rooms=this_rooms)
    #if not this_age == None:
       #data = data.filter(age=this_age)
    if data.count() < 50:
        return HttpResponse(' Sorry! There is not enough data about %s. just %i records are availbale!'%(this_location,data.count()))
    else:
        return JsonResponse(dumps({
            'message': ' OK! There is enough data about this location. just %i records are availbale!'%data.count(),
        }, ensure_ascii=False), safe=False , encoder=JSONEncoder)
           
#curl --data "offertype=1&location=سعادت آباد&area=100&age=0&rooms=2" http://localhost:8009/query/price/