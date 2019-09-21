# -*- coding: utf-8 -*-

import logging
import requests
import numpy as np
from sklearn import tree
from django.http import HttpResponse
from json import JSONEncoder,dumps
from django.shortcuts import render
from django.http import JsonResponse
from webscraper.models import PropertyFile
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

    data = PropertyFile.objects.filter(offertype=this_offertype,location__contains=this_location).order_by('-publishdate')
    #TODO: filter data with other criterea due to data.count()
    #TODO: prediction model. save result of prediction
    #TODO: search prediction history before start prediction
    #TODO: token provided or something to prevent robots

    if data.count()< 50:
        return JsonResponse({
            'message': 'There is not enogh data for this location',
        }, encoder=JSONEncoder)        

    count = data.count() if data.count()<150 else 150  # max 150 recordes are needed for prediction
    x = []
    y = []
    #asnwer =
    if this_offertype == '1':   # load input and output lists for prediction with last 150 record in database( MAX)
        for j in range(0, count):
            x.append([data[j].area, data[j].rooms,data[j].age])
            y.append(data[j].price1)
    elif this_offertype == '2':
        for j in range(0, count):
            x.append([data[j].area, data[j].rooms,data[j].age])
            y.append([data[j].price1,data[j].price2])
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(x,y)
    answer = clf.predict([[this_area,this_rooms,this_age]])
    if this_offertype == '1':
        return JsonResponse({
            'count' : '%i'%data.count(),
            'answer': 'I predict its cost as %i tomans'%answer[0],
            }, encoder=JSONEncoder)
    else:
        return JsonResponse({
            'count' : '%i'%data.count(),
            'answer': 'I predict its cost as %i tomans for deposit and %i tomans as monthly rent'%(answer[0][1],answer[0][0]),
            }, encoder=JSONEncoder)
    #logger.debug('%s %s %s %s %s'%(this_offertype,this_location,this_area,this_age,this_rooms))
    


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