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
#from django.urls import include, path
from django.conf.urls import url, include
#from django.urls import path
from django.contrib import admin
#from simpleapp1.admin import admin_site
#from simpleapp1 import views

urlpatterns = [
    url(r'^admin/', admin.site.urls), # required to overcome NoReverseMatch found error
    url(r'^autoscale/', include('simpleapp1.urls')),
#     url(r'^$', views.index, name='index'),
#     url(r'^cpuload/', views.overload_cpu, name='overload_cpu'),
#     url(r'^killpid/(?P<procid>[0-9]+)/$',views.kill_load,name='kill_load'),
    #url(r'^business/', views.business, name='business'),
]
