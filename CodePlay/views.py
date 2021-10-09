import random
from django import db
from django.db import models
from django.forms.models import model_to_dict
import requests
import json
import Backend.settings as settings
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import redirect, render
import django.contrib.auth.models as AuthModels
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.db.models import Q
from django.utils import timezone
from CodePlay.models.Accounts import SessionPool, User
from CodePlay.models.Paint import Scheme

from utils.Accounts import getSessionId, setSessionId, verifySessionId

# Create your views here.


def userinfo(req):
    
    if req.method == 'GET':
        sessionId = req.GET.get('sessionId')
        queryId = req.GET.get('student_id')
        if not sessionId:
            return HttpResponseBadRequest('Please query with sessionId')
        user = verifySessionId(sessionId)
        if not user:
            return HttpResponseBadRequest(json.dumps({"err": "not_logged_in"}))
        if user['role'] == 'User':
            user.pop('_state')
            return HttpResponse(json.dumps(user, ensure_ascii=False))
        else:
            if not queryId:
                user.pop('_state')
                return HttpResponse(json.dumps(user, ensure_ascii=False))
            else:
                qUser = User.objects.filter(student_id=queryId).first()
                if not qUser:
                    return HttpResponseBadRequest(json.dumps({"err": "not_found"}))
                qUser.pop('_state')
                return HttpResponse(json.dumps(qUser, ensure_ascii=False))
    else:
        # Verify and promote to Designer with 339BD665D02F8C3E8DD262B59D67A904
        POST = json.loads(req.body)
        sessionId = POST.get('sessionId')
        key = POST.get('key')
        if not sessionId:
            return HttpResponseBadRequest('Please query with sessionId')
        sessionRecord = SessionPool.objects.filter(sessionId=sessionId).first()
        if not sessionRecord:
            return HttpResponseBadRequest(json.dumps({"err": "not_logged_in"}))
        user = sessionRecord.user
        if (not key):
            return HttpResponseBadRequest('bad request')
        if key != '339BD665D02F8C3E8DD262B59D67A904':
            return HttpResponse(json.dumps({"status": "key verification failed"}, ensure_ascii=False))
        user.role = "Designer"
        user.save()
        dic = user.__dict__
        dic.pop('_state')
        return HttpResponse(json.dumps(dic, ensure_ascii=False))

def userScheme(req):
    if req.method == 'GET':
        # Read color scheme
        sessionId = req.GET.get('sessionId')
        queryId = req.GET.get('student_id')
        sortStrategy = req.GET.get('sort_strategy')
        if not sessionId:
            return HttpResponseBadRequest('Please query with sessionId')
        user = verifySessionId(sessionId)
        if not user:
            return HttpResponseBadRequest(json.dumps({"err": "not_logged_in"}))

        if queryId and user['role'] == 'Designer':
            qUser = User.objects.filter(student_id=queryId).first()
            if not qUser:
                    return HttpResponseBadRequest(json.dumps({"err": "not_found"}))
        user.pop('_state')
        result = {"request_user": user}
        if qUser:
            user = qUser
        try:
            user.pop('_state')
        except:
            pass
        result['user'] = user
        
        # Get all color schemes for user
        if result['request_user']['role'] == 'User':
            SchemeList = Scheme.objects.filter(hidden=False).filter(author_id=user['id']).all()
        else:
            SchemeList = Scheme.objects.filter(author_id=user['id']).all()
        # Sort
        sortDict = {
            "submission_time": (lambda x : x['submission_time'], False),
            "vote": (lambda x: x['likes'], True),
            "hue": (lambda x: x['colors'][0][4], False ),
        }
        try:
            sortMethod = sortDict[sortStrategy]
        except:
            sortMethod = sortDict['submission_time']
        sortedSchemeList = sorted(SchemeList, key=sortMethod[0], reverse=sortMethod[1])
        result['schemes'] = sortedSchemeList
        return HttpResponse(json.dumps(result, ensure_ascii=False))
    else:
        # Do operations on color scheme, including creating, editing, voting.
        POST = json.loads(req.body)
        sessionId=POST.get('sessionId')
        operation=POST.get('operation')
        schemeId=POST.get('id')
        name=POST.get('name')
        description=POST.get('description')
        colors = POST.get('colors')
        author_id = POST.get('author_id')
        sketch_id = POST.get('sketch_id')
        
        if operation == 'create':
            scheme = Scheme(sketch_id=sketch_id, name=name, description=description, author_id=author_id, colors=json.dumps(colors, ensure_ascii=False))
            scheme.save()
            dic = scheme.__dict__
            dic.pop('_state')
            return HttpResponse(json.dumps(dic, ensure_ascii=False))
        elif operation == 'update':

            scheme = Scheme.objects.filter(id=schemeId).first()
            if scheme:
                # Verify user permission
                if not sessionId:
                    return HttpResponseBadRequest('Please query with sessionId')
                user = verifySessionId(sessionId)
                if not user:
                    return HttpResponseBadRequest(json.dumps({"err": "not_logged_in"}))
                if scheme.author_id != user.student_id:
                    return HttpResponse(json.dumps({'status': 'permission denied'}))
                
                # Update properties
                if name:
                    scheme.name = name
                if description:
                    scheme.description = description
                if colors:
                    scheme.colors = json.dumps(colors, ensure_ascii=False)
                scheme.save()
                dic = scheme.__dict__
                dic.pop('_state')
                return HttpResponse(json.dumps(dic, ensure_ascii=False))
            else:
                return HttpResponse(json.dumps({'status': 'not found'}))
            
        elif operation == 'vote':
            scheme = Scheme.objects.filter(id=schemeId).first()
            if scheme:
                scheme.likes += 1
                scheme.save()
                dic = scheme.__dict__
                dic.pop('_state')
                return HttpResponse(json.dumps(dic, ensure_ascii=False))
            else:
                return HttpResponse(json.dumps({'status': 'not found'}))
            
        elif operation == 'approve':
            
            # Verify user permission
            if not sessionId:
                return HttpResponseBadRequest('Please query with sessionId')
            user = verifySessionId(sessionId)
            if not user:
                return HttpResponseBadRequest(json.dumps({"err": "not_logged_in"}))
            if user['role'] != 'Designer':
                return HttpResponse(json.dumps({'status': 'permission denied'}))

            scheme = Scheme.objects.filter(id=schemeId).first()
            if scheme:
                scheme.approved = True
                scheme.save()
                dic = scheme.__dict__
                dic.pop('_state')
                return HttpResponse(json.dumps(dic, ensure_ascii=False))
            else:
                return HttpResponse(json.dumps({'status': 'not found'}))
            
        elif operation == 'disapprove':
            
            # Verify user permission
            if not sessionId:
                return HttpResponseBadRequest('Please query with sessionId')
            user = verifySessionId(sessionId)
            if not user:
                return HttpResponseBadRequest(json.dumps({"err": "not_logged_in"}))
            if user['role'] != 'Designer':
                return HttpResponse(json.dumps({'status': 'permission denied'}))

            scheme = Scheme.objects.filter(id=schemeId).first()
            if scheme:
                scheme.approved = False
                scheme.save()
                dic = scheme.__dict__
                dic.pop('_state')
                return HttpResponse(json.dumps(dic, ensure_ascii=False))
            else:
                return HttpResponse(json.dumps({'status': 'not found'}))

        elif operation == 'delete':
            deletedScheme = Scheme.objects.filter(id=schemeId).first()
            if deletedScheme:
                
                # Verify user permission
                if not sessionId:
                    return HttpResponseBadRequest('Please query with sessionId')
                user = verifySessionId(sessionId)
                if not user:
                    return HttpResponseBadRequest(json.dumps({"err": "not_logged_in"}))
                if deletedScheme.author_id != user.student_id:
                    return HttpResponse(json.dumps({'status': 'permission denied'}))
                
                deletedScheme.hidden = True
                deletedScheme.save()
                dic = deletedScheme.__dict__
                dic.pop('_state')
                return HttpResponse(json.dumps(dic, ensure_ascii=False))
            else:
                return HttpResponse(json.dumps({'status': 'not found'}))

def exploreScheme(req):
    sketch_id = req.GET.get('sketch_id')
    sessionId = req.GET.get('sessionId')
    sortStrategy = req.GET.get('sort_strategy')
    approvedOnly = req.GET.get('approved')
    if not sessionId:
        return HttpResponseBadRequest('Please query with sessionId')
    if not sketch_id:
        return HttpResponseBadRequest('Please query with sketch_id')
    user = verifySessionId(sessionId)
    if not user:
        return HttpResponseBadRequest(json.dumps({"err": "not_logged_in"}))

    result = {"schemes": []}
    if user['role'] == 'Designer':
        
        # Approved Only
        schemeList = Scheme.objects.all()
        if approvedOnly:
            schemeList = schemeList.filter(approved=True)

        # Sort
        sortDict = {
            "submission_time": (lambda x: x['submission_time'], False),
            "vote": (lambda x: x['likes'], True),
            "hue": (lambda x: x['colors'][0][4], False),
            "designer_name": (lambda x: x['author']['name'], False)
        }
        try:
            sortMethod = sortDict[sortStrategy]
        except:
            sortMethod = sortDict['submission_time']
        
        length = len(schemeList)
        if length != 0:
            for i in range(0, length):
                dic = model_to_dict(schemeList[i])
                dic['colors'] = list(eval(dic['colors']))
                dic['author'] = model_to_dict(schemeList[i].author)
                result['schemes'].append(dic)
        result['schemes'] = sorted(result['schemes'], key=sortMethod[0], reverse=sortMethod[1])
        return HttpResponse(json.dumps(result, ensure_ascii=False))
    else:
        schemeList = Scheme.objects.filter(hidden=False)
        length = len(schemeList)
        if length != 0:
            i = random.randint(0, length-1)
            dic = schemeList[i].__dict__
            dic.pop('_state')
            dic['colors'] = list(eval(dic['colors']))
            result['schemes'].append(dic)
        return HttpResponse(json.dumps(result, ensure_ascii=False))
        
        
