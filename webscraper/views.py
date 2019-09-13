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
    scrapeIhomeBuy = Scrape(scrapetype= 'خرید-فروش')
    if scrapeIhomeBuy.startscraping():
        scrapeIhomeBuy.save()
    return HttpResponse('Hi...we are going to Store information about the house you want in database!')

