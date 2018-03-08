'''
Created on Jul 24, 2016

@author: bhujay
'''

from django import forms
from django.forms import  ModelForm, formset_factory
from django.forms import Textarea,CheckboxInput,SelectMultiple
from simpleapp1.models import Laptop,Order


class LaptopForm(ModelForm):
    selected = forms.BooleanField(label = 'Select', required=False)
    class Meta:
        model=Laptop
        fields='__all__'
        #exclude = ['os']
        
       
        