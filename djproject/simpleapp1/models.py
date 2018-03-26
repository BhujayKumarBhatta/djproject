# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Laptop(models.Model):
    laptopmodel=models.CharField(max_length=100)
    currentstock=models.CharField(max_length=100)
    totalstock=models.CharField(max_length=100)      
    def __unicode__(self):
        return self.laptopmodel
    


class Order(models.Model):
    ordernum=models.CharField(max_length=100)
    qty=models.CharField(max_length=16)
    laptop=models.ForeignKey(Laptop)      
    def __unicode__(self):
        return self.ordernum

class Openstack_Auth(models.Model):
    os_url = models.URLField(max_length=200)
    os_project_domain_name = models.CharField(max_length=100)
    os_user_domain_name = models.CharField(max_length=100)
    os_tenant_name = models.CharField(max_length=100)
    os_project_name = models.CharField(max_length=100)
    os_user_name = models.CharField(max_length=100)
    os_password = models.CharField(max_length=100)
    os_url_type = models.CharField(max_length=20, default='publicURL')
    os_stack_id = models.CharField(max_length=100)