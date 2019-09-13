# -*- coding: utf-8 -*-
import requests
import logging
from django.shortcuts import render
from django.http import HttpResponse
from .models import Scrape, PropertyFile
from datetime import datetime
from django.db.models import Max    

logger = logging.getLogger(__name__)

# Create your views here.
def collectdata(request):
    logger.debug("----def collectdata ----->  is running")
    last_update = PropertyFile.objects.all().aggregate(Max('publishdate'))
    logger.debug("----def collectdata last update is on  ----->  %s"%last_update)
    
    scrapeIhomeBuy = Scrape(scrapetype= 'خرید-فروش')
    if scrapeIhomeBuy.startscraping():
        scrapeIhomeBuy.save()
    return HttpResponse('Hi...we are going to Store information about the house you want in database!')

