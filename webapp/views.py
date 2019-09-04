from django.shortcuts import render
from django.http import JsonResponse
from json import JSONEncoder
from django.views.decorators.csrf import csrf_exempt
import requests
from .models import activationcode
from .utils import grecaptcha_verify
from django.contrib.auth.models import User

#creats a random code (for activating account)
random_str : lambda N:''.join(random.SystemRandom().\
    choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(N))


# Create your views here.
def manageRequestRegistrationCode(request):
   # if not grecaptcha_verify(request): #captcha is incorrect
   #     context = {'message' : 'دوست عزیز کپچا رو اشتباه زدی'}
   #     return render(request,'register.html',context)
    
    if User.objects.filter(email = request.POST['email']).exists():
        context = {'message' : 'این ایمیل از قبل ثبت شده! '} #TODO: link to login page
        return render(request,'register.html',context)
    
    if User.objects.filter(username = request.POST['username']).exists():
        context = {'message' : 'این نام کاربری تکراریه! لطفا یکی دیگه انتخاب کن.'}
        return render(request,'register.html',context)
    
    else: #captcha, email and username is ok
        context = {'message' : 'آفرین.'}
        return render(request,'register.html',context)

def manageClickingActivationLink(request):
    context = {'message': 'روی فرم کلیک شدهو برگشته'}
    return render(request,'register.html',context)  

def manageUnknownRequest(request)  :
    context = {'message': 'برای دسترسی به امکانات سایت باید عضو باشی. در 20 ثانیه ثبت نام کن'}
    return render(request,'register.html',context)
    


@csrf_exempt
def register (request):
    if request.method =='POST':
       # context = {'message': 'یک قدم به جلو برداشتی باز'}
       # return render(request,'register.html',context)
        return manageRequestRegistrationCode(request)
                 
    else:
        #return manageClickingActivationLink(request)
        return manageUnknownRequest(request)
   # if request.POST.has_key('requestcode'): #the client wants to register so send him a registration code
  #     return manageRequestRegistrationCode(request)
    
   # elif request.Get.has_key('code'):     #the client has clicked on activation link
   #   return manageClickingActivationLink(request)
    
  #  else:      #unknows request
   #     return manageUnknownRequest(request)
    

