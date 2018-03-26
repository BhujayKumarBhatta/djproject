'''
Created on Jul 24, 2016

@author: bhujay
'''

from django import forms
from django.forms import  ModelForm, formset_factory
from django.forms import Textarea,CheckboxInput,SelectMultiple ,PasswordInput
from simpleapp1.models import Laptop,Order,Openstack_Auth
from django.forms.widgets import NumberInput


class LaptopForm(ModelForm):
    selected = forms.BooleanField(label = 'Select', required=False)
    class Meta:
        model=Laptop
        fields='__all__'
        #exclude = ['os']
        
class OrderForm(ModelForm):
    #selected = forms.BooleanField(label = 'Select', required=False)
    class Meta:
        model=Order        
        fields= ['laptop', 'qty']
        widgets = {
            'qty': NumberInput(attrs={'size':20}),
        }
class OSAuthEditForm(ModelForm):
    #os_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=Openstack_Auth        
        fields='__all__'
        widgets = {
            'os_password': PasswordInput(),
            }

       
        