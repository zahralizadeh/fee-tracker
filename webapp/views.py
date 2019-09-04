from django.shortcuts import render
from django.http import JsonResponse
from json import JSONEncoder
from django.views.decorators.csrf import csrf_exempt
import requests
from .models import activationcode, Token
from .utils import grecaptcha_verify
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from datetime import datetime
# Create your views here.

@csrf_exempt
def register (request):
    if request.method =='POST':
        #TODO: start recaptcha
        # if not grecaptcha_verify(request): #captcha is incorrect
        # context = {'message' : 'دوست عزیز کپچا رو اشتباه زدی'}
        # return render(request,'register.html',context)

        if User.objects.filter(email = request.POST['email']).exists():
            context = {'message' : 'این ایمیل از قبل ثبت شده! '} #TODO: link to login page
            return render(request,'register.html',context)
    
        if User.objects.filter(username = request.POST['username']).exists():
            context = {'message' : 'این نام کاربری تکراریه! لطفا یکی دیگه انتخاب کن.'}
            return render(request,'register.html',context)
    
        else: #captcha, email and username is ok
            code = get_random_string(length=32)
            now = datetime.now()
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            temporary_user = activationcode(email=email,username=username,password=password,\
                code = code, time = now)
            temporary_user.save()
            #TODO send email to user
            context = {'message' : 'آفرین.'}
            return render(request,'register.html',context)
                 
    else:
        try:
            code = request.GET['code']
            
            #email = request.GET['email']
            if activationcode.objects.filter(code = code).exists():
                context = {'message': code}
                new_temp_user = activationcode.objects.get(code = code)
                new_user = User.objects.Create(username = new_temp_user.username,\
                    password = new_temp_user.password,
                    email = new_temp_user.email)
                token_code = get_random_string(length=48)
                token = Token.objects.Create(user = new_user, token = token_code)
                activationcode.objects.filter(code = code).delete()
            else: 
                context = {'message': 'invalid code   '+code}
            
        except:
            context = {'message': 'برای دسترسی به امکانات سایت باید عضو باشی. در 20 ثانیه ثبت نام کن'}
        return render(request,'register.html',context)
