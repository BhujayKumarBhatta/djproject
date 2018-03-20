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


from keystoneauth1 import loading , session
from novaclient import client as novaclient
from gnocchiclient import client as gclient
import datetime


from django.views.generic import ListView , DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy


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


def openstack_view(request):
    slist = []
    sdict = {}
    loader = loading.get_plugin_loader('password')
    auth = loader.load_from_options(auth_url='http://10.172.100.14:5000/v3',
                                     project_domain_name='itc',
                                     user_domain_name='itc',
                                     username='bbhatta',
                                     password='welcome@123',
                                     tenant_name='bhujay',
                                     project_name='bhujay',
                                     )
    sess = session.Session(auth=auth)
    nova = novaclient.Client('2', session=sess,endpoint_type='internalURL')
    gcon = gclient.Client('1', session=sess,
                           adapter_options={'connect_retries': 3,
                           'interface': 'internalURL'} )
    try:
        al = nova.servers.list()
        for s in al:
            if 'asg_name' in s.metadata and s.metadata['asg_name']=='autoscale_demo_1':
                for net in s.to_dict()['addresses'][s.networks.keys()[0]]:
                    if net['OS-EXT-IPS:type']=='floating':
                        sdict['fip'] = net['addr']
                    else:
                        sdict['pip'] = net['addr']
                    sdict['sobj'] = s
                slist.append(sdict)
                
    except:
        pass
    context = {'slist': slist}
    return render(request, 'openstack_view.html', context)
   

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
    

