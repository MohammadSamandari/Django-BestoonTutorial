# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.
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
    User= models.ForeignKey(User)
    def __unicode__(self):
        return "{}-{}".format(self.date,self.amount)
        # this function is returing the string to be shown in the admin page in the models title.


