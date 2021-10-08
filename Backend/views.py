import time
import math
import datetime
from django.http.response import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
import django.contrib.auth.models as AuthModels
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.db.models import Q
from django.utils import timezone

# Create your views here.


def index(req):
    sessionId = req.COOKIES.get('sessionId', 'DoesNotExist')
    props = {"page": {"sessionId": sessionId}}
    print(props)
    return render(req, "base.html", props)
