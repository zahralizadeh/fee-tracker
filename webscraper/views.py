# -*- coding: utf-8 -*-
import requests
import logging
from django.shortcuts import render
from django.http import HttpResponse
from .models import Scrape, PropertyFile
from datetime import datetime

logger = logging.getLogger(__name__)

# Create your views here.
def collectdata(request):
    logger.debug("----def collectdata ----->  is running")
    scrapeIhomeBuy = Scrape(pagetarget=1,pagenumber=1,currnetrecord=0,startTime=datetime.now,\
        endTime=datetime.now,status='initialied',scrapetype= 'خرید-فروش',site='ihome' )
    scrapeIhomeBuy.startscraping() 
    return HttpResponse('Hi...we are going to Store information about the house you want in database!')

