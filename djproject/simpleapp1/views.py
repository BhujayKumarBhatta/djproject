# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
import socket

import subprocess
from subprocess import  PIPE
from multiprocessing import Pool
from multiprocessing import cpu_count
import psutil
import time
from django.template.defaultfilters import join

from simpleapp1.forms import LaptopForm, OrderForm
from models import Laptop, Order
from django.forms import formset_factory,modelformset_factory,inlineformset_factory

process_pid_list = []
ctag = []
def index(request):   
    hostname = socket.gethostname()
    ipaddr = socket.gethostbyname(hostname)
    FormSetLaptop=modelformset_factory(Laptop,LaptopForm,extra=0)
    if request.method == 'POST':
        selected_itmes = request.POST.getlist('selected[]')
        dtag={'laptopmodelid':request.POST.get("laptopmodelid",""),
                              'laptopmodel':request.POST.get("laptopmodel",""),
                              'totalstock':(request.POST.get("totalstock",0)),
                              'currentstock':(request.POST.get("currentstock",0)),
                              'selected':(request.POST.get("selected",""))
                              }
        s1= ("ID:- "+ dtag['laptopmodelid']+ " Model:- "+ dtag['laptopmodel']+"  Total Stock: "+ dtag['totalstock']+ 
        " Avilable :- "+ dtag['currentstock']+ " Item Selected : - "+dtag['selected'])
        
        formset = FormSetLaptop(request.POST,request.FILES)        
        if formset.is_valid():            
            tmpformset = formset.save(commit=False)
            for tmpform in tmpformset:
                    #if tmpform.selected == True:
                        
                        rec = {'laptopmodelid':tmpform.laptopmodelid,'laptopmodel':tmpform.laptopmodel,
                               'totalstock':tmpform.totalstock,'currentstock':tmpform.currentstock} #'Selection_Status':tmpform.selected
                        #rec = tmpform.ip
                        #tmpform.save()
                        ctag.append(rec)
                
            #ftag.append(ctag)  
        
        return HttpResponse(ctag)
    else:
        laptop_inventory = FormSetLaptop()
        
    context = {'hostname': hostname, 
               'ipaddr': ipaddr , 
               'cpu_util': psutil.cpu_percent(),
               'laptop_inventory': laptop_inventory,
               }
    #return HttpResponse("Hostname of this Web Server  is %s and Ip Address is %s " %(hostname, ipaddr))
    return render(request, 'homepage.html', context)

def business(request):    
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            lapdop_data = order_form.cleaned_data['laptop']
            laptop_object = Laptop.objects.get(laptopmodel = lapdop_data )
            laptop_id = laptop_object.id
            current_stock = int(laptop_object.currentstock)
            order_qty = int(order_form.cleaned_data['qty'])
            if  order_qty <= current_stock:
                updated_stock = current_stock-order_qty
                laptop_object.currentstock = updated_stock
                laptop_object.save()
                msg = (' %s number of %s Laptop Order has been Booked. Updated  available stock is %s '
                       % (str(order_qty),
                            lapdop_data,
                            str(updated_stock)                                    
                                   ) 
                         )
            else:
                 msg = ("%s  numbers of %s Laptop are not available in stock, Try different model or reduce quantity below %s" 
                         % (str(order_qty),
                            lapdop_data,
                            str(current_stock)                                    
                                   ) 
                         )                 
            
            return HttpResponse(msg)                                    
                                
    else:
        order_form = OrderForm()
    context = {'order_form': order_form}
    return render(request,'business.html', context)



def f(x):
    while True:
        x*x

def overload_cpu(request):
    hostname = socket.gethostname()
    ipaddr = socket.gethostbyname(hostname)
#    processes = cpu_count()
#     print('utilizing %s cores:' % str(processes))
#     print(psutil.cpu_percent())
#     pool = Pool(processes)
#     pool.map(f(1000), range(processes))
    #proc = subprocess.Popen(['/bin/sh', '/home/bhujay/x.sh'], stdout=PIPE, stderr=PIPE)
    #proc = subprocess.Popen(['cat', '/dev/zero', '>', '/dev/null'])
    proc = subprocess.Popen(['dd', 'if=/dev/zero', 'of=/dev/null'])
    process_pid_list.append(proc.pid)    
    context = {'hostname': hostname, 
               'ipaddr': ipaddr ,
               'cpu_core': cpu_count(), 
               'cpu_util': psutil.cpu_percent(), 
               'process_pid_list': process_pid_list}
    return render(request, 'overload_cpu.html', context )
    #return HttpResponse("Will slap you ")
#
def kill_load(request, procid):
    hostname = socket.gethostname()
    ipaddr = socket.gethostbyname(hostname)
    p = subprocess.Popen(["kill", "-9",  procid]) 
    
    try:
        process_pid_list.remove(int(procid))
    except:
        pass
    
    context = {'hostname': hostname, 
               'ipaddr': ipaddr ,
               'cpu_core': cpu_count(), 
               'cpu_util': psutil.cpu_percent(), 
               'process_pid_list': process_pid_list}
    return render(request, 'killed_process.html', context )
    #return HttpResponse(l)
