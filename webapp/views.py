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
        #TODO: upgrade recaptcha
        if not grecaptcha_verify(request): #captcha is incorrect
            context = {'message' : 'دوست عزیز کپچا رو اشتباه زدی'}
            return render(request,'register.html',context)

        if User.objects.filter(email = request.POST['email']).exists():
            context = {'message' : 'این ایمیل از قبل ثبت شده! '} #TODO: link to login page or resend activation code
            return render(request,'register.html',context)
    
        if User.objects.filter(username = request.POST['username']).exists():
            context = {'message' : 'این نام کاربری تکراریه! لطفا یکی دیگه انتخاب کن.'}
            return render(request,'register.html',context)
    
        else: #captcha, email and username is ok
            code = get_random_string(length=28)
            now = datetime.now()
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            temporary_user = activationcode(email=email,username=username,password=password,\
                code = code, time = now)
            temporary_user.save()
            #TODO send email to user
            
            message = 'قدیم ها ایمیل فعال سازی می فرستادیم ولی الان شرکتش ما رو تحریم کرده (: پس راحت و بی دردسر'
            body = " برای فعال کردن اکانت بستون خود روی لینک روبرو کلیک کنید: <a href=\"?code={}\">لینک رو به رو</a> ".format(code)
            message = message + body
            context = {
                'message': message }
            return render(request,'register.html',context)
                 
    else:
        try:
            code = request.GET['code']
            
            #email = request.GET['email']
            if activationcode.objects.filter(code = code).exists():
                
                new_temp_user = activationcode.objects.get(code = code)             
                new_user = User.objects.create(username = new_temp_user.username,password = new_temp_user.password,email = new_temp_user.email)
                token_code = get_random_string(length=48)
                user_token = Token.objects.create(user = new_user, token = token_code)
                activationcode.objects.filter(code = code).delete()
                context = {'message': 'ثبت نام شما با موفقیت انجام شد. برای ادامه در سایت لاگین کنید'}
            else: 
                context = {'message': 'متاسفانه این کد فعال سازی معتبر نمی باشد. برای عضویت در سایت دوباره فرم ثبت نام را پر کنید.'+code}
            
        except:
            context = {'message': 'برای دسترسی به امکانات سایت باید عضو باشی. در کمتر از 20 ثانیه ثبت نام کن'}
        return render(request,'register.html',context)


@csrf_exempt
def login (request):
    if request.method =='POST':
        #TODO: upgrade recaptcha
        if not grecaptcha_verify(request): #captcha is incorrect
            context = {'message' : 'دوست عزیز کپچا رو اشتباه زدی'}
            return render(request,'login.html',context)
        
        username =  request.POST['username'] #save request parameters
        password =  request.POST['password']
        
        if not User.objects.filter(email = username).exists():  #not valid email entered
            if not User.objects.filter(username = username).exists(): #not valid email & username entered
                message ='نام کاربری یا کلمه عبور صحیح نیست. دوباره تلاش کنید. در صورتی که قبلا حساب کاربری باز نکرده اید  <a href=\"register\">اینجا</a> کلیک کنید  '
                context = {'message' : message}
                return render(request,'login.html',context)
            else: #valid username entered
                user_account =  User.objects.get(username = username)        
        else:  #valid email entered
            user_account =  User.objects.get(email = username)                 
        
        if not user_account.password == password : #valid username but invalid password
            message ='نام کاربری یا کلمه عبور صحیح نیست. دوباره تلاش کنید. در صورتی که قبلا حساب کاربری باز نکرده اید  <a href=\"register\">اینجا</a> کلیک کنید  '
            context = {'message' : message}
            return render(request,'login.html',context)        
        else: #valid username & password
            message = 'تبریک! با موفقیت وارد شدید'
            context = {'message': message }
            return render(request,'login.html',context)
