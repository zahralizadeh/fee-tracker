# -*- coding: utf-8 -*-
import requests
import logging
from django.shortcuts import render
from django.http import HttpResponse
from .models import Scrape, PropertyFile
from datetime import datetime
from django.db.models import Max,Min 

logger = logging.getLogger(__name__)

# Create your views here.
def collectdata(request):
    logger.debug("----def collectdata ----->  is running")
    last_property_time = PropertyFile.objects.all().aggregate(Max('publishdate'))
    first_property = PropertyFile.objects.all().aggregate(Min('publishdate'))
    
    logger.debug("----def collectdata last saved property is published on  ----->  %s"%last_property)
    logger.debug("----def collectdata last saved property is published on  ----->  %s"%first_property)

    scrapeIhomeBuy = Scrape(scrapetype= 'خرید-فروش')
    if scrapeIhomeBuy.startscraping_update():
        scrapeIhomeBuy.save()
    return HttpResponse('Hi...we are going to Store information about the house you want in database!')

