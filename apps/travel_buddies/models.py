from __future__ import unicode_literals

from django.db import models
import bcrypt
from datetime import datetime


# Create your models here.
class usersManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        print postData
        if len(postData['name']) < 2:
            errors['name'] = 'Please enter a valid name'
        if len(postData['userName']) < 2:
            errors['userName'] = 'Please enter a valid name'
        if len(postData['password']) < 2:
            errors['password'] = 'Please enter a valid password'
        if postData['password'] != postData['confirm_pw']:
            errors['confirm_pw'] = 'Your passwords do not match'
        return errors
    def login(self, postData):
        errors = {}
        user = Users.objects.filter(userName=postData['username'])
        print user
        if user is None:
            errors['username'] = 'Invalid username'
        elif not bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
            errors['password'] = 'Invalid password please try again'
        return errors

class tripsManager(models.Manager):
    def trip_validator(self, postData):
        print datetime.today().date()
        print 'postData {}'.format(datetime.strptime(postData['date_from'], '%Y-%m-%d').date())
        errors = {}
        if len(postData['destination']) < 3:
            errors['desination'] = 'Please enter a valid desination'
        elif len(postData['description']) < 10:
            errors['description'] = 'Description was not long enought please add more to description'
        elif datetime.strptime(postData['date_from'], '%Y-%m-%d').date() < datetime.today().date():
            errors['date_from'] = 'Travel dates must be in the future please try again'
        elif datetime.strptime(postData['date_to'], '%Y-%m-%d').date() < datetime.strptime(postData['date_from'], '%Y-%m-%d').date():
            errors['date_to'] = 'End of trip must be after start of trip'
        return errors


class Users(models.Model):
    name = models.CharField(max_length=255)
    userName = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    objects = usersManager()


class Trips(models.Model):
    destination = models.CharField(max_length=255)
    description = models.TextField()
    date_from = models.DateField()
    date_to = models.DateField()
    user = models.ManyToManyField(Users, related_name='trips', blank=True)
    primaryuser = models.ForeignKey(Users, related_name='planner', default=None)
    objects = tripsManager()