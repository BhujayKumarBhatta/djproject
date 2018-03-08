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

