import random
from typing import cast
from django import db
from django.db import models, reset_queries
from django.forms.models import model_to_dict
import requests
import json
import Backend.settings as settings
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect, render
import django.contrib.auth.models as AuthModels
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.db.models import Q
from django.utils import timezone
from CodePlay.models.Accounts import SessionPool, User
from CodePlay.models.Paint import Scheme, Sketch

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
            return JsonResponse(({"err": "not_logged_in"}))
        if user['role'] == 'User':
            user.pop('_state')
            return JsonResponse((user))
        else:
            if not queryId:
                user.pop('_state')
                return JsonResponse((user))
            else:
                qUser = User.objects.filter(student_id=queryId).first()
                if not qUser:
                    return HttpResponseBadRequest(json.dumps({"err": "not_found"}))
                qUser.pop('_state')
                return JsonResponse((qUser))
    else:
        # Verify and promote to Designer with 339BD665D02F8C3E8DD262B59D67A904
        POST = json.loads(req.body)
        print(POST)
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
        if key != '339bd665d02f8c3e8dd262b59d67a904':
            return JsonResponse(({"status": "key verification failed"}))
        user.role = "Designer"
        user.save()
        dic = user.__dict__
        dic.pop('_state')
        return JsonResponse((dic))

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
            qUser = User.objects.filter(student_id=queryId).first().__dict__
            if not qUser:
                    return HttpResponseBadRequest(json.dumps({"err": "not_found"}))
        user.pop('_state')
        result = {"request_user": user}
        try:
            if qUser:
                user = qUser
            user.pop('_state')
        except:
            pass
        result['user'] = user
        
        # Get all color schemes for user
        if result['request_user']['role'] == 'User':
            SchemeList = Scheme.objects.filter(hidden=False).filter(
                author_id=user['student_id']).all()
        else:
            SchemeList = Scheme.objects.filter(author_id=user['student_id']).all()
        # Sort
        sortDict = {
            "submission_time": (lambda x : x.submission_time, False),
            "vote": (lambda x: x.likes, True),
            "hue": (lambda x: list(eval(x.colors))[0][4], False ),
        }
        try:
            sortMethod = sortDict[sortStrategy]
        except:
            sortMethod = sortDict['submission_time']
        sortedSchemeList = sorted(SchemeList, key=sortMethod[0], reverse=sortMethod[1])
        result['schemes'] = []
        for scheme in sortedSchemeList:
            dic = dict(scheme.__dict__)
            dic.pop('_state')
            dic['author'] = dict(scheme.author.__dict__)
            dic['author'].pop('_state')
            result['schemes'].append(dic)
        return JsonResponse((result))
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
            
            # Verify no schemes under the same user with the same name
            
            scheme_list_ = Scheme.objects.filter(author_id=author_id).filter(sketch_id=sketch_id)
            for another_scheme in scheme_list_:
                if another_scheme.name == name:
                    return JsonResponse({"err": "name duplicated"})
            
            
            # Verify no similar schemes
            scheme_list_ = Scheme.objects.filter(hidden=False).filter(sketch_id=sketch_id)
            for another_scheme in scheme_list_:
                this_primary = colors
                another_scheme_primary = json.loads(another_scheme.colors)
                similar = 0
                
                for index, color in enumerate(this_primary):
                    deltaR = this_primary[index][0]-another_scheme_primary[index][0]
                    deltaG = this_primary[index][1]-another_scheme_primary[index][1]
                    deltaB = this_primary[index][2]-another_scheme_primary[index][2]
                    
                    deltaR **=2
                    deltaG **=2
                    deltaB **=2
                    
                    if deltaR <= 64 and deltaG <= 64 and deltaB <= 64 and (deltaR + deltaB + deltaG) <= 144:
                        similar += 1
                if similar == len(this_primary):
                    return JsonResponse({"err": "similar"})
            
            
            scheme = Scheme(sketch_id=sketch_id, name=name, description=description, author_id=author_id, colors=json.dumps(colors))
            scheme.save()
            dic = scheme.__dict__
            dic.pop('_state')
            return JsonResponse((dic))
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
                    return JsonResponse(({'status': 'permission denied'}))
                
                # Update properties
                if name:
                    scheme.name = name
                if description:
                    scheme.description = description
                if colors:
                    scheme.colors = json.dumps(colors)
                scheme.save()
                dic = scheme.__dict__
                dic.pop('_state')
                return JsonResponse((dic))
            else:
                return JsonResponse(({'status': 'not found'}))
            
        elif operation == 'vote':
            
            # Verify user permission
            if not sessionId:
                return HttpResponseBadRequest('Please query with sessionId')
            user = verifySessionId(sessionId)
            if not user:
                return HttpResponseBadRequest(json.dumps({"err": "not_logged_in"}))

            scheme = Scheme.objects.filter(id=schemeId).first()
            
            if scheme:
                try:
                    people = scheme.voted_people.get(student_id=user['student_id'])
                    return JsonResponse({'err': 'already_liked'})
                except:
                    scheme.likes += 1
                    scheme.voted_people.add(user['student_id'])
                    scheme.save()
                    dic = model_to_dict(scheme)
                    dic.pop('voted_people')
                    dic['liked'] = True
                    return JsonResponse(dic)
            else:
                return JsonResponse(({'err': 'not found'}))
            
        elif operation == 'unvote':
            
            # Verify user permission
            if not sessionId:
                return HttpResponseBadRequest('Please query with sessionId')
            user = verifySessionId(sessionId)
            if not user:
                return HttpResponseBadRequest(json.dumps({"err": "not_logged_in"}))

            scheme = Scheme.objects.filter(id=schemeId).first()
            
            if scheme:
                try:
                    people = scheme.voted_people.get(student_id=user['student_id'])
                    if people:
                        scheme.likes -= 1
                        scheme.voted_people.remove(user['student_id'])
                        scheme.save()
                        dic = model_to_dict(scheme)
                        print(dic)
                        dic.pop('voted_people')
                        dic['liked'] = False
                        return JsonResponse(dic)
                    else:
                        raise ""
                    
                except:
                    return JsonResponse({'err': 'not_liked'})

            else:
                return JsonResponse(({'err': 'not found'}))
            
        elif operation == 'approve':
            
            # Verify user permission
            if not sessionId:
                return HttpResponseBadRequest('Please query with sessionId')
            user = verifySessionId(sessionId)
            if not user:
                return HttpResponseBadRequest(json.dumps({"err": "not_logged_in"}))
            if user['role'] != 'Designer':
                return JsonResponse(({'status': 'permission denied'}))

            scheme = Scheme.objects.filter(id=schemeId).first()
            if scheme:
                scheme.approved = True
                scheme.save()
                dic = scheme.__dict__
                dic.pop('_state')
                return JsonResponse((dic))
            else:
                return JsonResponse(({'status': 'not found'}))
            
        elif operation == 'disapprove':
            
            # Verify user permission
            if not sessionId:
                return HttpResponseBadRequest('Please query with sessionId')
            user = verifySessionId(sessionId)
            if not user:
                return HttpResponseBadRequest(json.dumps({"err": "not_logged_in"}))
            if user['role'] != 'Designer': 
                return JsonResponse(({'status': 'permission denied'}))

            scheme = Scheme.objects.filter(id=schemeId).first()
            if scheme:
                scheme.approved = False
                scheme.save()
                dic = scheme.__dict__
                dic.pop('_state')
                return JsonResponse((dic))
            else:
                return JsonResponse(({'status': 'not found'}))

        elif operation == 'delete':
            deletedScheme = Scheme.objects.filter(id=schemeId).first()
            if deletedScheme:
                
                # Verify user permission
                if not sessionId:
                    return HttpResponseBadRequest('Please query with sessionId')
                user = verifySessionId(sessionId)
                if not user:
                    return HttpResponseBadRequest(json.dumps({"err": "not_logged_in"}))
                if deletedScheme.author_id != user['student_id']:
                    return JsonResponse(({'status': 'permission denied'}))
                
                deletedScheme.hidden = True
                deletedScheme.save()
                dic = deletedScheme.__dict__
                dic.pop('_state')
                return JsonResponse((dic))
            else:
                return JsonResponse(({'status': 'not found'}))

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
        
    # Approved Only
    schemeList = Scheme.objects.all()
    #schemeList = [model_to_dict(i) for i in schemeListRaw]
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
            voted = schemeList[i].voted_people
            dic = model_to_dict(schemeList[i])
            try:
                voted.get(student_id=user['student_id'])
                dic['liked'] = True
            except:
                dic['liked'] = False
            
            dic.pop('voted_people')
            dic['colors'] = list(eval(dic['colors']))
            dic['author'] = model_to_dict(schemeList[i].author)
            result['schemes'].append(dic)
    result['schemes'] = sorted(result['schemes'], key=sortMethod[0], reverse=sortMethod[1])
    return JsonResponse((result))

def sketch(req):
    sketchList = Sketch.objects.filter(hidden=False).all()
    result = []
    for i in sketchList:
        result.append( model_to_dict(i) )
    return JsonResponse({"sketch_list": result})
