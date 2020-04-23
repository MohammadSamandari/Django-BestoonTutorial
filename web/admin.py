# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Expense, Income
# Register your models here.
admin.site.register(Expense)
# this add the income model to the admin page of the app.
admin.site.register(Income)

