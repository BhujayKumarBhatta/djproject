# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import socket


def index(request):
    hostname = socket.gethostname()
    ipaddr = socket.gethostbyname(hostname)
    return HttpResponse("Hostname of this Web Server  is %s and Ip Address is %s " %(hostname, ipaddr))