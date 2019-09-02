from django.shortcuts import render
from django.http import JsonResponse
from json import JSONEncoder
from django.views.decorators.csrf import csrf_exempt
import requests
from views import activationcode


# Create your views here.

def manageRequestRegistrationCode(request):
    
    
@csrf_exempt
def register (request):

    if request.POST.haskey('requestcode'):
        #the client wants to register so send him a registration code
        return manageRequestRegistrationCode(request)
    elif request.Get.has_key('code'):
        #the client has clicke on activation link
        return manageClickingActivationLink()
    else:
        #unknows request
        return manageUnknownRequest()
    

