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

from simpleapp1.forms import LaptopForm
from models import Laptop, Order
from django.forms import formset_factory,modelformset_factory,inlineformset_factory

process_pid_list = []

def index(request):   
    hostname = socket.gethostname()
    ipaddr = socket.gethostbyname(hostname)
    FormSetLaptop=modelformset_factory(Laptop,LaptopForm,extra=0)
    if request.method == 'POST':
        dtag={'laptopmodelid':request.POST.get("laptopmodelid",""),
                              'laptopmodel':request.POST.get("laptopmodel",""),
                              'totalstock':(request.POST.get("totalstock",0)),
                              'currentstock':(request.POST.get("currentstock",0)),
                              }
        s1= "ID:- "+ dtag['laptopmodelid']+ " Model:- "+ dtag['laptopmodel']+"  Total Stock: "+ dtag['totalstock']+ " Avilable :- "+ dtag['currentstock']
        return HttpResponse(s1)
    else:
        laptop_inventory = FormSetLaptop()
        
    context = {'hostname': hostname, 
               'ipaddr': ipaddr , 
               'cpu_util': psutil.cpu_percent(),
               'laptop_inventory': laptop_inventory,
               }
    #return HttpResponse("Hostname of this Web Server  is %s and Ip Address is %s " %(hostname, ipaddr))
    return render(request, 'homepage.html', context)

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
