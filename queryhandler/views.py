# -*- coding: utf-8 -*-

import logging
import requests
from json import JSONEncoder
from django.shortcuts import render
from django.http import JsonResponse
from webscraper.models import PropertyFile
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


logger = logging.getLogger(__name__)

# Create your views here.
@csrf_exempt
@require_POST
def query_price(request):
    this_offertype = request.POST['offertype']
    this_location = request.POST['location']
    this_area = int(request.POST['area'])
    this_rooms = int(request.POST['rooms'])
    this_age = int(request.POST['age']) if 'age' in request.POST else None
    #TODO: validate user input
    data = PropertyFile.objects.filter(offertype=this_offertype)
    #location__contains=this_location,,area=this_area,rooms=this_rooms)
    #if not this_age == None:
       #data = data.filter(age=this_age)
    if data.count() < 50:
        return JsonResponse({
            'message': ' Sorry! There is not enough data about this location. just %i records are availbale!'%data.count(),
        }, encoder=JSONEncoder)
    else:
        return JsonResponse({
            'message': ' OK! There is enough data about this location. just %i records are availbale!'%data.count(),
        }, encoder=JSONEncoder)
    result= [list(i) for i in data]
    x = []
    y = []
    if this_offertype == 'خرید_فروش':
        if not this_age == None:
            for j in result:
                x.append([j.location, j.area, j.rooms])
                #x.append([j[k] for k in range(3)])
                y.append(j.price1)
        else:
            for j in result:
                x.append([j.location, j.area, j.rooms,j.age])
                #x.append([j[k] for k in range(3)])
                y.append(j.price1)
    
    #logger.debug('%s %s %s %s %s'%(this_offertype,this_location,this_area,this_age,this_rooms))
    return JsonResponse({
        'number of data': '%i %i'%(len(x),len(y)),
    }, encoder=JSONEncoder)
#curl --data "offertype=1&location=سعادت آباد&area=100&age=0&rooms=2" http://localhost:8009/query/price/