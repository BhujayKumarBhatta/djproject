"""djproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
#from django.urls import path
from django.contrib import admin
from simpleapp1 import views
#from simpleapp1.admin import admin_site

app_name = 'simpleapp1'
urlpatterns = [
    url(r'^admin/', admin.site.urls, name="admin"),    
    url(r'^$', views.index, name='index'),
    #url('', views.index, name='index'),
    url(r'^cpuload/', views.overload_cpu, name='overload_cpu'),
    url(r'^killpid/(?P<procid>[0-9]+)/$',views.kill_load,name='kill_load'),
    url(r'^inventory/$', views.Inventory.as_view(), name='inventory'),
    url(r'^inventory/add/$', views.InventoryAdd.as_view(), name='inventory_add'),
    url(r'^inventory/update/(?P<pk>[\w-]+)$', views.InventoryUpdate.as_view(), name='inventory_update'),
    url(r'^openstack/', views.openstack_view, name='openstack'),
    url(r'^osauth/$', views.OSauth.as_view(), name='osauth'),
    url(r'^osauth/add/$', views.OSauthAdd.as_view(), name='osauth_add'),
    url(r'^osauth/update(?P<pk>[\w-]+)$', views.OSauthUpdate.as_view(), name='osauth_update'),
    
    #url(r'^business/', views.business, name='business'),
]
