# -*- coding: utf-8 -*-
import requests
import logging
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Max,Min 
from datetime import datetime,timedelta
from .models import Scrape, PropertyFile
from django.utils.timezone import make_aware

logger = logging.getLogger(__name__)

# Create your views here.
def collectdata(request):
    logger.debug("----def collectdata ----->  is running")
    try:    #property database is not empty
        last_property_time = PropertyFile.objects.order_by('-publishdate')[0].publishdate
        first_property = PropertyFile.objects.order_by('publishdate')[0].publishdate
    
        logger.debug("----def collectdata, the last saved property is published on  ----->  %s"%last_property_time)
        logger.debug("----def collectdata, the first last property is published on  ----->  %s"%first_property)

        scrapeIhomeBuy = Scrape(scrapetype= 'خرید-فروش',last_update_time=last_property_time)
        if scrapeIhomeBuy.startscraping_update():
            scrapeIhomeBuy.save()
        return HttpResponse('Hi...we are going to Store information about the house you want in database!')
    except: 
        if  not PropertyFile.objects.all():
            scrapeIhomeBuy = Scrape(scrapetype= 'خرید-فروش',last_update_time=make_aware(datetime.now() - timedelta(days=60)))
            if scrapeIhomeBuy.startscraping_update():
                scrapeIhomeBuy.save() 
                return HttpResponse('Hi...Database was empty! last onth Data scraped successfully!')
        return HttpResponse('Hi...There was an error in process of collecting data!')

