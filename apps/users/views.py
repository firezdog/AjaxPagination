# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import math
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.shortcuts import render, redirect
from django.contrib import messages
from models import User
from django.core.urlresolvers import reverse
from django.http import JsonResponse

def error_form_serialization(error_dict):
    plain_dict = dict([(k, [unicode(e) for e in v]) for k,v in error_dict.items()])
    return simplejson.dumps(plain_dict)

#/users/
def index(request):
    number_users = len(User.objects.all())
    users = User.objects.all()[:5]
    users_pages = int(math.ceil(number_users/5.0))
    display_range = range(0,users_pages)
    page_map = {}
    for i in display_range:
        page_map[i] = i+1
    context = {
        'users': users,
        'page_map': page_map
    }
    return render(request, 'index.html', context)

#/users/ajax-index
def ajaxIndex(request):
    users = User.objects.all().values('first_name','last_name','email','created_at')
    #users = json.dumps(list(users), cls=DjangoJSONEncoder)
    users = list(users)
    errors = list(messages.get_messages(request))
    processedErrors = []
    for error in errors: 
        processedErrors.append(error.message)
    data = {'users': users, 'errors': processedErrors}
    return JsonResponse(data)

#/users/create (my_create)
def create(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
    else:
        first = request.POST['first_name']
        last = request.POST['last_name']
        email = request.POST['email'].lower()
        User.objects.create(first_name = first, last_name = last, email = email)
    return redirect('/users/ajax-index')

def destroy(request, id):
    User.objects.get(id=id).delete()
    return redirect('/users')

def update(request):
    id = request.POST['user']
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect(reverse('my_edit',kwargs={'id':id}))
    else:    
        first = request.POST['first_name']
        last = request.POST['last_name']
        email = request.POST['email'].lower()
        u = User.objects.get(id=id)
        u.first_name = first
        u.last_name = last
        u.email = email
        u.save()
        return redirect('/users')