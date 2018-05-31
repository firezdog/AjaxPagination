# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re

email_regex = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if not(len(postData['first_name']) or len(postData['last_name'])):
            errors['name_length'] = "First and last name fields cannot be blank."
        elif not(postData['first_name'].isalpha() or postData['last_name'].isalpha()):
            errors['name_form'] = "First and last name fields accept letters only."
        if not email_regex.match(postData['email']):
            errors['email'] = "Email address is invalid."
        if len(User.objects.filter(email=postData['email'].lower()).exclude(id=postData['user'])):
            errors['unique'] = "Email address already exists in database."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()