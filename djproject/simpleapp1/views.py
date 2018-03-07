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

hostname = socket.gethostname()
ipaddr = socket.gethostbyname(hostname)


def index(request):    
    context = {'hostname': hostname, 
               'ipaddr': ipaddr , 
               'cpu_util': psutil.cpu_percent()}
    #return HttpResponse("Hostname of this Web Server  is %s and Ip Address is %s " %(hostname, ipaddr))
    return render(request, 'homepage.html', context)



def f(x):
    while True:
        x*x

def overload_cpu(request):
#    processes = cpu_count()
#     print('utilizing %s cores:' % str(processes))
#     print(psutil.cpu_percent())
#     pool = Pool(processes)
#     pool.map(f(1000), range(processes))
    proc = subprocess.Popen(['/bin/sh', '/home/bhujay/x.sh', '&'], stdout=PIPE, stderr=PIPE)
    context = {'hostname': hostname, 
               'ipaddr': ipaddr ,
               'cpu_core': cpu_count(), 
               'cpu_util': psutil.cpu_percent(), 
               'process_pid': proc.pid}
    return render(request, 'overload_cpu.html', context )
    #return HttpResponse("Will slap you ")
#
def kill_load(request, procid):
    p = subprocess.Popen(["kill", "-9",  procid])
    context = {'hostname': hostname, 
               'ipaddr': ipaddr ,
               'cpu_core': cpu_count(), 
               'cpu_util': psutil.cpu_percent(), 
               'process_pid': procid}
    return render(request, 'killed_process.html', context )
