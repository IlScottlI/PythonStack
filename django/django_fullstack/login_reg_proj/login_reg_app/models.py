from django.db import models
from django.contrib import messages
import re


class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First Name must be longer than 2 characters'
        else:
            FIRST_NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
            if not FIRST_NAME_REGEX.match(postData['first_name']):
                errors['first_name'] = 'First name can contain letters only'
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last Name must be longer than 2 characters'
        else:
            LAST_NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
            if not LAST_NAME_REGEX.match(postData['last_name']):
                errors['last_name'] = 'Last name can contain letters only'
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        elif len(User.objects.filter(email=postData['email'])) > 0:
            errors['email'] = "Email is already registered"
        if len(postData['password']) < 8:
            errors['password'] = 'Password should be at least 8 characters'
        else:
            if postData['password'] != postData['password']:
                errors['password'] = 'Passwords do not match'
        if len(postData['password_repeat']) < 8:
            errors['password_repeat'] = 'Password should be at least 8 characters'
        else:
            if postData['password_repeat'] != postData['password']:
                errors['password_repeat'] = 'Passwords do not match'
        return errors

    def login_validator(self, postData):
        errors = {}
        try:
            userAccount = User.objects.filter(email=postData['login_email'])[0]
            print(userAccount)
        except:
            print('Account Not Found')
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['login_password']) < 8:
            errors['login_password'] = "Check Password and try again"
        if not EMAIL_REGEX.match(postData['login_email']):
            errors['login_email'] = "Invalid email address!"
        elif len(User.objects.filter(email=postData['login_email'])) < 1:
            errors['login_email'] = "Email is not registered"
        else:
            userAccount = User.objects.filter(email=postData['login_email'])[0]
            print(userAccount)
            if postData['login_password'] != userAccount.password:
                errors['login_password'] = "Check Password and try again"
        print(errors)
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
