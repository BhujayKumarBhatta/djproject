# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin 
from django.contrib.admin  import AdminSite
from models import Laptop, Order

# Register your models here.

# class Laptopdeco(admin.ModelAdmin):
#     list_display = ('laptopmodel','currentstock','totalstock')
# 
# admin.site.register(Laptop,Laptopdeco)
#registering in views through admin class view

@admin.register(Laptop)
class LaptopAdmin(admin.ModelAdmin):
    fields = ('laptopmodel','currentstock','totalstock')
    list_display = ('laptopmodel','currentstock','totalstock')


# class LaptopAdmin(AdminSite):
#     fields = ('laptopmodel','currentstock','totalstock')
#     list_display = ('laptopmodel','currentstock','totalstock')
#     site_url = 'http://192.168.111.130:9999/autoscale/'
#  
# admin_site = LaptopAdmin(name = 'laptopadmin')
# 
# admin_site.register(Laptop)


# class LaptopAdmin(AdminSite):
#     fields = ('laptopmodel','currentstock','totalstock')
#     list_display = ('laptopmodel','currentstock','totalstock')
#     site_url = 'autoscale/'
#   
# admin_site = LaptopAdmin(name = 'laptopadmin')
# 
# admin_site.register(Laptop)

 
