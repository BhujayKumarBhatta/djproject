# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.template.defaultfilters import join

from models import Openstack_Auth
from keystoneauth1 import loading , session
from novaclient import client as novaclient
from gnocchiclient import client as gclient
from aodhclient.v2 import client as aclient
import datetime , time

# openstack minitoring view  with graphs
def openstack_graph_func():              
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
        td = datetime.timedelta(hours=5, minutes=30)
        for s in al:
            xlist = []    
            if 'asg_name' in s.metadata and s.metadata['asg_name']=='autoscale_demo_1':
                try:
                    #Gnocchi data collection for the server s 
                    all_cpu_util_values=gcon.metric.get_measures('cpu_util',resource_id=s.id) 
                    for cpu_util_value in all_cpu_util_values:
                       udate, xgran, xutil = cpu_util_value
                       xdate = udate+td
                       xdict = {'xdate': int(time.mktime(xdate.timetuple())), 'xutil': xutil }
                       xlist.append(xdict)
                except:
                    all_cpu_util_values = []                    
                    xlist = []                      
                try:
                    list_of_ips=s.networks.itervalues().next()
                    fixedip=list_of_ips[0]
                    floatip=list_of_ips[1]
                except:
                    fixedip='getting prepared'
                    floatip='getting prepared'
                    
                #Create the various key value parameters for server
                sdict = {'sobj': s, 'fixedip': fixedip, 
                         'floatip': floatip, 'xlist': xlist }
                #add all the servers key value in a list for template to unpack 
                slist.append(sdict)                  
    except:
        pass
    alist = []
    ahistory_with_localtime = []
    td = datetime.timedelta(hours=5, minutes=30)
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
               for h in ahistory_with_utc:
                   htime = datetime.datetime.strptime(h['timestamp'], '%Y-%m-%dT%H:%M:%S.%f')
                   htime_local = htime+td
                   ht_str = htime_local.strftime('%Y-%m-%dT%H:%M:%S.%f')
                   ahistory_with_localtime.append({'timestamp': ht_str, 'detail': h['detail']})
               adict = {'aid': aid, 'aname': aname, 'ahistory': ahistory_with_localtime }
               alist.append(adict)
    except:
        pass
    context = {'slist': slist, 'alist': alist}
    return context
   


