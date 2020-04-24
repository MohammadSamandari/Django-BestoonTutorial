# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#Token Class
class Token(models.Model):
    # each user has a token and each token is connected to a user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
        # the on delete part, removes the token when the user is removed, so any extra data is not registered.
    token = models.CharField(max_length=48)
    def __unicode__(self):
        return "{}_Token".format(self.user)


class Expense(models.Model):
    text = models.CharField(max_length=255)
    date = models.DateTimeField()
    amount = models.BigIntegerField()
    user = models.ForeignKey(User)
    def __unicode__(self):
        return "{}-{}".format(self.date,self.amount)


# this is the model for the income.
class Income(models.Model):
    text = models.CharField(max_length=255)
    date = models.DateTimeField()
    amount = models.BigIntegerField()
    user= models.ForeignKey(User)
    def __unicode__(self):
        return "{}-{}".format(self.date,self.amount)
        # this function is returing the string to be shown in the admin page in the models title.


