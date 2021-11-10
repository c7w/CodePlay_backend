import time
import math
import datetime
from django import db
from django.db import models
import requests
import Backend.settings as settings
from django.http.response import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
import django.contrib.auth.models as AuthModels
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.db.models import Q
from django.utils import timezone
from CodePlay.models.Accounts import SessionPool, User

from utils.Accounts import getSessionId, setSessionId, verifySessionId

# Create your views here.


def index(req):
    sessionId = getSessionId(req)
    
    # If sessionId does not exist, then the user cannot be logged in
    if not sessionId:
        res = redirect('/login')
        setSessionId(res)
        return res
    
    user = verifySessionId(sessionId)
    if user:
        return render(req, 'index.html')
    else:
        return render(req, 'login.html')
    
    

def login(req):
    sessionId = getSessionId(req)
    if not sessionId:
        res = redirect('/login')
        setSessionId(res)
        return res
    
    # Verify if the sessionId has been binded to a certain user
    user = verifySessionId(sessionId)
    if user:
        return redirect('/')
    
    # Step 1
    code = req.GET.get('code')
    if not code:
        return redirect(f'https://stu.cs.tsinghua.edu.cn/api/v2/authorize?response_type=code&client_id=8pKCWELExLFMkeqA4qZ8cpNItD0&redirect_uri={settings.WEB_URL}/login')
    
    # Step 2
    clientInfo = {
        "client_id": "8pKCWELExLFMkeqA4qZ8cpNItD0",
        "client_secret": "shfKjrGJeS9EsYFlDHuQ",
        "code": code,
        "redirect_uri": f"{settings.WEB_URL}/login"
    }
    access_token = requests.post('https://stu.cs.tsinghua.edu.cn/api/v2/access_token', json=clientInfo).json()['access_token']
    
    # Step 3
    userinfo = requests.get(
        f'https://stu.cs.tsinghua.edu.cn/api/v2/userinfo?access_token={access_token}').json()['user']
    # Find the user with certain StuID
    user = User.objects.filter(student_id=userinfo['student_id']).first()
    if not user:
        # Create user
        user = User.objects.create(student_id=userinfo['student_id'], name=userinfo['name'],
                    fullname=userinfo['fullname'], email=userinfo['email'])
    # Bind sessionId to user
    sessionRecord = SessionPool.objects.create(sessionId=sessionId, user=user)
    return redirect('/')

def logout(req):
    sessionId = getSessionId(req)
    # If sessionId does not exist, then the user cannot be logged out
    if not sessionId:
        res = redirect('/')
        setSessionId(res)
        return res
    sessionRecord = SessionPool.objects.filter(sessionId=sessionId).first()
    if sessionRecord:
        SessionPool.objects.filter(sessionId=sessionId).delete()
        return redirect('/')
    else:
        return redirect('/')
