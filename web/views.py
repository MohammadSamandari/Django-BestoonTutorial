# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests

from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from json import JSONEncoder
from django.views.decorators.csrf import csrf_exempt
from web.models import User , Token, Expense , Income, Passwordresetcodes
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from postmark import PMMail
from django.contrib.auth.hashers import make_password
import random
import string
import time

# Create your views here.

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def grecaptcha_verify(request):
    data = request.POST
    captcha_rs = data.get('g-recaptcha-response')
    url = "https://www.google.com/recaptcha/api/siteverify"
    params = {
        'secret': settings.RECAPTCHA_SECRET_KEY,
        'response': captcha_rs,
        'remoteip': get_client_ip(request)
    }
    verify_rs = requests.get(url, params=params, verify=True)
    verify_rs = verify_rs.json()
    return verify_rs.get("success", False)

random_str = lambda N: ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(N))

def register(request):
    if request.POST.has_key('requestcode'): #form is filled. if not spam, generate code and save in db, wait for email confirmation, return message
        #is this spam? check reCaptcha
        if not grecaptcha_verify(request): # captcha was not correct
            context = {'message': 'کپچای گوگل درست وارد نشده بود. شاید ربات هستید؟ کد یا کلیک یا تشخیص عکس زیر فرم را درست پر کنید. ببخشید که فرم به شکل اولیه برنگشته!'} #TODO: forgot password
            return render(request, 'register.html', context)

        if User.objects.filter(email = request.POST['email']).exists(): # duplicate email
            context = {'message': 'متاسفانه این ایمیل قبلا استفاده شده است. در صورتی که این ایمیل شما است، از صفحه ورود گزینه فراموشی پسورد رو انتخاب کنین. ببخشید که فرم ذخیره نشده. درست می شه'} #TODO: forgot password
            #TODO: keep the form data
            return render(request, 'register.html', context)

        if not User.objects.filter(username = request.POST['username']).exists(): #if user does not exists
            code = random_str(28)
            now = datetime.now()
            email = request.POST['email']
            password = make_password(request.POST['password'])
            username = request.POST['username']
            temporarycode = Passwordresetcodes (email = email, time = now, code = code, username=username, password=password)
            temporarycode.save()
            '''message = PMMail(api_key = settings.POSTMARK_API_TOKEN,
                                subject = "فعال سازی اکانت بستون",
                                sender = "jadi@jadi.net",
                                to = email,
                                text_body = "برای فعال سازی ایمیلی بستون خود روی لینک روبرو کلیک کنید: http://iran-parts.ir/bestoon/register/?email={}&code={}".format(email, code),
                                tag = "acouunt request")
            message.send()
            context = {'message': 'ایمیلی حاوی لینک فعال سازی اکانت به شما فرستاده شده، لطفا پس از چک کردن ایمیل، روی لینک کلیک کنید.'}'''

            if Passwordresetcodes.objects.filter(code=code).exists(): #if code is in temporary db, read the data and create the user
                new_temp_user = Passwordresetcodes.objects.get(code=code)
                newuser = User.objects.create(username=new_temp_user.username, password=new_temp_user.password, email=email)
                this_token = random_str(48)
                token=Token.objects.create(user= newuser, token= this_token)
                Passwordresetcodes.objects.filter(code=code).delete() #delete the temporary activation code from db
                context = {'message': 'اکانت شما ساخته شد. توکن شما {} است. آن را ذخیره کنید چون دیگر نمایش داده نخواهد شد! جدی'.format(this_token)}
                return render(request, 'login.html', context)
            else:
                context = {'message': 'این کد فعال سازی معتبر نیست. در صورت نیاز دوباره تلاش کنید'}
                return render(request, 'login.html', context)
            
            return render(request, 'login.html', context)
        else:
            context = {'message': 'متاسفانه این نام کاربری قبلا استفاده شده است. از نام کاربری دیگری استفاده کنید. ببخشید که فرم ذخیره نشده. درست می شه'} #TODO: forgot password
            #TODO: keep the form data
            return render(request, 'register.html', context)
        '''elif request.GET.has_key('code'): # user clicked on code
        logger.debug("def register code: " + format(request.GET))
        email = request.GET['email']
        code = request.GET['code']
        if Passwordresetcodes.objects.filter(code=code).exists(): #if code is in temporary db, read the data and create the user
            new_temp_user = Passwordresetcodes.objects.get(code=code)
            newuser = User.objects.create(username=new_temp_user.username, password=new_temp_user.password, email=email)
            this_token = random_str(48)
            token=Token.objects.create(user= newuser, token= this_token)
            Passwordresetcodes.objects.filter(code=code).delete() #delete the temporary activation code from db
            context = {'message': 'اکانت شما ساخته شد. توکن شما {} است. آن را ذخیره کنید چون دیگر نمایش داده نخواهد شد! جدی'.format(this_token)}
            return render(request, 'login.html', context)
        else:
            context = {'message': 'این کد فعال سازی معتبر نیست. در صورت نیاز دوباره تلاش کنید'}
            return render(request, 'login.html', context)'''
    else:
        context = {'message': ''}
        return render(request, 'register.html', context)


@csrf_exempt
def submit_income(request):
    this_token = request.POST['token']
    this_user= User.objects.filter(token__token=this_token).get()
    if 'date' not in request.POST:
        date=datetime.now()
    
    Income.objects.create(user= this_user, amount= request.POST['amount'], text=request.POST['text'], date=date)
     
    return JsonResponse({
        'status':'ok',
    
    }, encoder=JSONEncoder)


def index(request):
    context={}
    return render(request,'index.html',context)

@csrf_exempt
def submit_expense(request):
    # request is all the data that user has send with any method.
    ''' User submits an expense '''

    # TODO: Validate data, user might be fake, token might be fake , amount might be fake, amount might ne ...

    this_token = request.POST['token']
    this_user = User.objects.filter(token__token = this_token).get()
    if 'date' not in request.POST:
        date=datetime.now()
    
    Expense.objects.create(user= this_user, amount= request.POST['amount'], text=request.POST['text'], date=date)
    
    return JsonResponse({
        'status': 'ok',
    }, encoder= JSONEncoder)

