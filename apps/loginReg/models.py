from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, ValidationError
import re, bcrypt, time

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')


# Create your models here.
class UserManager(models.Manager):
    def login(self, data):
        error = []
        if not len(data['username']) >= 3 or not data['username'].isalpha():
            error.append("Username must be greater than length of 3 and can only contain letter")
        if len(data['password']) < 8:
            error.append('Password must be at least 8 characters long')

        try:
            registered_info = User.objects.get(username=data['username'])
            registered_password = registered_info.password
            if not bcrypt.checkpw(data['password'].encode(), registered_password.encode()):
                error.append("Password does not match. YOU IMPOSTER!")
        except:
            error.append("Username does not Exist. Please register for an account")

        if error:
            return (False, error, False)

        return (True, "Succesful login", registered_info)


    #User validations
    def register(self, data):
        error = []
        if not len(data['name']) >= 3 or not data['name'].isalpha():
            error.append("Name must be greater than length of 3 and can only contain letter")
        if not len(data['username']) >= 3 or not data['username'].isalpha():
            error.append("Username must be greater than length of 3 and can only contain letter")
        if len(data['password']) < 8:
            error.append('Password must be at least 8 characters long')
        if data['password'] != data['password']:
            error.append('Passwords must match')
        #add validation for date hired. import time?
        if not data['date']:
            error.append("Please enter a date that can't be in the future. Unless you can time travel. Then it's totally cool")
        if error:
            #return error list of messages
            return (False, error, False)

        #Now check is registered user_email already exists in database
        try:
            user_name = data['username']
            db_user= User.objects.get(username = user_name)
            if db_user.username == user_name:
                error.append("Username already exists. Please use a different username")
                return (False, error, False)
        except:
            print "Username is new! Carry on"
            pass


        password = data['password'].encode()
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        register_user = User.objects.create(name = data['name'], username=data['username'], date_hired = data['date'] ,password = hashed)

        return (True, "Succesful login!", register_user)


class User(models.Model):
    name = models.CharField(max_length =45)
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    date_hired = models.DateField(auto_now=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
