# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import Laptop, Order

# Register your models here.

class Laptopdeco(admin.ModelAdmin):
    list_display = ('laptopmodel','currentstock','totalstock')

admin.site.register(Laptop,Laptopdeco)

