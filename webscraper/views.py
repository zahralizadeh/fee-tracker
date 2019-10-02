# -*- coding: utf-8 -*-

import requests
import logging
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime,timedelta
from .models import Scrape, PropertyFile
from django.utils.timezone import make_aware

logger = logging.getLogger(__name__)

# Create your views here.
def collectdata(request):
    try:
        this_offertype = request.GET['offertype']
    except:
        this_offertype = 'all'
        logger.debug("----def collectdata ----->  Collecting both BUY and RENT Files!")
    response = 'Hi..\n'

    if this_offertype in (2,'2'):
        logger.debug("----def collectdata BUY ----->  IGNORE RUNNING")
    else:
        logger.debug("----def collectdata BUY ----->  is running")
        try:    #property database is not empty
            
            last_buy_property_time = PropertyFile.objects.filter(offertype = 1).order_by('-publishdate')[0].publishdate
            scrapeIhomeBuy = Scrape(scrapetype= 'خرید-فروش',last_update_time=last_buy_property_time)
            logger.debug("----def collectdata BUY -----> scrapeIhomeBuy initialized")
            if scrapeIhomeBuy.startscraping_update():
                scrapeIhomeBuy.save()
                response = response +'I saved information about offertype = Buy in database!' 
            else: 
                scrapeIhomeBuy.save() 
                response = response + 'ERROR in startscraping_update!'  
        except: 
            if  not PropertyFile.objects.filter(offertype = 1): #property database is  empty
                scrapeIhomeBuy = Scrape(scrapetype= 'خرید-فروش',last_update_time=make_aware(datetime.now() - timedelta(days=60)))
                if scrapeIhomeBuy.startscraping_update():
                    scrapeIhomeBuy.save() 
                    response = response + 'There was no BUY files saved in DB! Data published in the last month was scraped successfully!'
                else: 
                    scrapeIhomeBuy.save() 
                    response = response + 'There was no BUY files saved in DB! ERROR in startscraping_update!'
            else:
                response = response + 'There was an error in process of collecting  BUY data!'
    
    if this_offertype in (1, '1'):
        logger.debug("----def collectdata RENT ----->  IGNORE RUNNING")
    else:
        logger.debug("----def collectdata RENT ----->  is running")
        try:
            last_rent_property_time = PropertyFile.objects.filter(offertype = 2).order_by('-publishdate')[0].publishdate
            scrapeIhomeRent = Scrape(scrapetype= 'رهن-اجاره',last_update_time=last_rent_property_time)
            logger.debug("----def collectdata RENT -----> scrapeIhomeRent initialized")

            if scrapeIhomeRent.startscraping_update():
                scrapeIhomeRent.save()
                response = response +'\n I saved information about offertype = Rent in database!'
            else: 
                scrapeIhomeBuy.save() 
                response = response + 'ERROR in startscraping_update!'
        except: 
            if  not PropertyFile.objects.filter(offertype = 2): #property database is  empty
                scrapeIhomeRent = Scrape(scrapetype= 'رهن-اجاره',last_update_time=make_aware(datetime.now() - timedelta(days=60)))
                if scrapeIhomeRent.startscraping_update():
                    scrapeIhomeRent.save() 
                    response = response +'\n There was no RENT files saved in DB! Data published in the last month was scraped successfully!'
                else:
                    scrapeIhomeBuy.save() 
                    response = response + 'There was no RENT files saved in DB! ERROR in startscraping_update!'
            else:
                response = response + '\n There was an error in process of collecting  RENT data!'
    return HttpResponse(response)
