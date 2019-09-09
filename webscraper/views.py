import requests
import logging
from django.shortcuts import render
from django.http import HttpResponse

logger = logging.getLogger(__name__)

# Create your views here.
def collectdata(request):
    logger.debug("----def collectdata is running")
    return HttpResponse('Hi...we are going to Store information about the house you want in database!')

