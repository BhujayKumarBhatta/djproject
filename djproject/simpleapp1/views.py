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
from models import Laptop, Order, Openstack_Auth
from django.forms import formset_factory,modelformset_factory,inlineformset_factory


from keystoneauth1 import loading , session
from novaclient import client as novaclient
from gnocchiclient import client as gclient
from aodhclient.v2 import client as aclient
import datetime


from django.views.generic import ListView , DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
import forms

from simpleapp1.openstack_graph_module import openstack_graph_func


process_pid_list = []

def index(request):  
    laptop_all = Laptop.objects.all()
    order_all = Order.objects.all()  
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
                try:
                    laptop_object.currentstock = updated_stock
                    laptop_object.save()
                    order_rec = Order(laptop=laptop_object, qty=order_qty)
                    order_rec.save()
                    order_number = order_rec.id
                except django.db.Error as e:
                    print (str(e))
                    
                msg = (' %s number of %s Laptop Order has been Booked.Your Order Number is : - %s. Updated  available stock is %s '
                       % (str(order_qty),
                            lapdop_data,
                            str(order_number),
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
            context = {'laptop_all': laptop_all, 'order_all': order_all, 'msg': msg,
                       'hostname': socket.gethostname(), 
                       'ipaddr': socket.gethostbyname(socket.gethostname()) , 
                       'cpu_util': psutil.cpu_percent(),}
            #return HttpResponse(msg)
            return render(request,'business.html', context)                                    
                                
    else:
        order_form = OrderForm()
    context = {'order_form': order_form,'laptop_all': laptop_all, 'order_all': order_all,
               'hostname': socket.gethostname(), 
               'ipaddr': socket.gethostbyname(socket.gethostname()) , 
               'cpu_util': psutil.cpu_percent(),}
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

# openstack minitoring view 
def openstack_view(request):
    try:
        conf=Openstack_Auth.objects.get(pk=1)
        loader = loading.get_plugin_loader('password')
        auth = loader.load_from_options(auth_url= conf.os_url,
                                     project_domain_name= conf.os_project_domain_name,
                                     user_domain_name=  conf.os_user_domain_name,
                                     username=  conf.os_user_name,
                                     #password= conf.os_password,
                                     password= conf.os_password_encrypt,
                                     tenant_name= conf.os_tenant_name,
                                     project_name= conf.os_project_name, 
                                     )
        sess = session.Session(auth=auth)
        nova = novaclient.Client('2', session=sess,endpoint_type= conf.os_url_type)
        gcon = gclient.Client('1', session=sess,
                           adapter_options={'connect_retries': 3,
                           'interface': conf.os_url_type} )
        al = nova.servers.list()
        slist = []
        for s in al:
            xlist = []    
            if 'asg_name' in s.metadata and s.metadata['asg_name']=='autoscale_demo_1':
                try:
                    #Gnocchi data collection for the server s 
                    all_cpu_util_values=gcon.metric.get_measures('cpu_util',resource_id=s.id)     
                    vdate, vgran, cutil = all_cpu_util_values[-1]
                    vdatef = vdate.strftime('%Y-%m-%d %H:%M:%S')
                    for cpu_util_value in all_cpu_util_values:
                       xdate, xgran, xutil = cpu_util_value
                       xdict = {'xdate': xdate.strftime('%Y-%m-%d %H:%M:%S'), 'xutil': xutil}
                       xlist.append(xdict)
                except:
                    all_cpu_util_values = []
                    vdatef, vgran, cutil = ('try after 10 Minutes', 'try after 10 Minutes', 'try after 10 Minutes')
                    xlist = []
                    
                try:
                    list_of_ips=s.networks.itervalues().next()
                    fixedip=list_of_ips[0]
                    floatip=list_of_ips[1]
                except:
                    fixedip='getting prepared'
                    floatip='getting prepared'
                    
                #Create the various key value parameters for server s
                sdict = {'sobj': s, 'fixedip': fixedip, 'floatip': floatip, 
                  'collection_time' : vdatef, 'cutil': cutil,
                  'all_cpu_util_values': all_cpu_util_values,
                  'xlist': xlist }
                #add all the servers key value in a list for template to unpack 
                slist.append(sdict)  
                
    except:
        pass
    alist = []
    try:
        acon =  aclient.Client(session=sess,interface= 'internalURL')
        for myalarm in acon.alarm.list():
           rule=myalarm['gnocchi_aggregation_by_resources_threshold_rule']
           rq=rule['query']
           #if 'f447c07f-ff7b-48b8-924b-ff7220e20c0b' in rq:
           if conf.os_stack_id in rq:
               aid = myalarm['alarm_id']
               aname = myalarm['name']
               ahistory = acon.alarm_history.get(aid)
               adict = {'aid': aid, 'aname': aname, 'ahistory': ahistory }
               alist.append(adict)
    except:
        pass
    context = {'slist': slist, 'alist': alist}
    return render(request, 'openstack_view.html', context)

def openstack_graph_view(request):
    context = openstack_graph_func()
    return render(request, 'openstack_graph_template', context)
   
# Iventory addition and update by the store manager
class Inventory(ListView):
    model = Laptop
    template_name = 'inventory.html'
    
class InventoryAdd(CreateView):
    model = Laptop
    fields = ['laptopmodel', 'currentstock']
    template_name = 'InventoryAdd.html'
    success_url = reverse_lazy('simpleapp1:inventory')
    
class InventoryUpdate(UpdateView):
    model = Laptop
    fields = ['laptopmodel', 'currentstock']
    template_name = 'InventoryUpdate.html'
    success_url = reverse_lazy('simpleapp1:inventory')    

#Configuration setting for connecting to openstack controller and retrive monoitoring data     
class OSauth(ListView):
    model = Openstack_Auth
    fields = '__all__'
    template_name = 'osauth.html'
    
class OSauthAdd(CreateView):
    model = Openstack_Auth
    #fields = '__all__'
    form_class = forms.OSAuthEditForm
    template_name = 'osauth_add.html'
    success_url = reverse_lazy('simpleapp1:osauth')

class OSauthUpdate(UpdateView):
    model = Openstack_Auth
    #fields = '__all__'
    form_class = forms.OSAuthEditForm
    template_name = 'osauth_add.html'
    success_url = reverse_lazy('simpleapp1:osauth')
    

    
        
    

