# -*- coding: utf-8 -*-

import logging
import requests
from datetime import datetime, timedelta
from json import JSONEncoder
from django.shortcuts import render
from django.utils.timezone import make_aware
from .models import PropertyPredictResponse
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


logger = logging.getLogger(__name__)

# Create your views here.
@csrf_exempt
def query_price(request):
    try:
        this_offertype = request.GET['offertype']
        this_location = request.GET['location']
        this_area = int(request.GET['area'])
        this_rooms = int(request.GET['rooms'])
        this_age = int(request.GET['age']) 
    except: 
        #TODO: handle responces by serializer     #http://www.tomchristie.com/rest-framework-2-docs/tutorial/1-serialization
        
        #Return a 400 response if the data was invalid.
        return JsonResponse({
            'status': '400 Bad Request ',
            'message': 'Make sure you have sent correct data & try again!',
            }, encoder=JSONEncoder)

    #TODO: Treshhold should be manged in admin panel
    available_response = PropertyPredictResponse.objects.filter(\
        location =this_location, offertype=this_offertype, area=this_area, age=this_age, rooms=this_rooms, \
        responseDate__gte=make_aware(datetime.now() - timedelta(days=7)))
    if available_response.count() > 0:
        #TODO: do it by serializer
        response = available_response.order_by('-responseDate')[0]
        response.hotPlus()
        response.save()
        return response.send_response()

    else:
        #TODO: token provided or something to prevent robots
        prediction =PropertyPredictResponse(location =this_location, offertype=this_offertype, area=this_area,\
            age=this_age, rooms=this_rooms)
        response = prediction.predict()
        prediction.save()
        return response
    
       


@csrf_exempt
def whatisprice(request):
    pass
           
