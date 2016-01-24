#!/usr/bin/env python
# -*- coding: utf-8 -*-
##########################################################################
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
#
##########################################################################
"""
This module provide configure file management service in i18n environment.

Authors: liyingpeng(liyingpeng@baidu.com)
Date:    2016/01/20 17:23:06
"""
import socket
import json
import sys
from threading import Thread

from django.http import HttpResponse
from django.shortcuts import render_to_response

import dataparser as dataparser


port = 8089
socket_dic = {}
dataparser = dataparser.DataParser()


def adddata(request):
    """
    Django funciton to deal with http request(add data request)
    """
    if request.method == 'POST':
        data = request.POST['viewdescription']
        global local_ip
        local_ip = request.POST['local_ip']
        filename = local_ip + '.txt'
        with open(filename, 'wt') as f:
            f.write(data.encode('utf-8'))
        f.close()

    ip = socket.gethostbyname(socket.gethostname())
    if 'sock_serv' not in globals():
        global sock_serv
        try:
            sock_serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as error:
            print 'Failed to create socket. Error code: ' + error.message
            sys.exit()
        print 'a sock_serv is created'
        sock_serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_serv.bind((ip, port))
        sock_serv.listen(5)

    def _accept():
        sock, addr = sock_serv.accept()
        client_ip = addr[0]
        if client_ip in socket_dic:
            socket_dic[client_ip].close()
            print 'the old connect has closed'
            socket_dic[client_ip] = sock
        else:
            socket_dic[client_ip] = sock
        print 'add data session'
        request.session['isconnected'] = 1
        print request.session['isconnected']

    t = Thread(target=_accept)
    t.start()

    return HttpResponse('True')


def showdata(request):
    """
    Django funciton to deal with http request(show data request)
    """
    print 'show data session'
    if 'isconnected' in request.session:
        print request.session['isconnected']
    else:
        print 'no isconnected'

    filename = local_ip + '.txt'
    with open(filename, 'rt') as f:
        data = f.read()
    f.close()

    jsonData = dataparser.parsedata(data)

    context = {
        'jsonData': jsonData,
        'client_ip': local_ip,
        'isconnected': '1'
    }
    return render_to_response('index.html', context)


def buildView(request):
    if request.method == 'POST':
        data = request.body
        dataObj = json.loads(data)
    return render_to_response('view.html', dataObj)


def statusChange(request):
    """
    Django funciton to deal with http request(change status request)
    """
    if request.method == 'POST':
        data = request.body
        dataObj = json.loads(data)
        client_ip = dataObj['client_ip']
        command = dataObj['command']
        if command == 'disconnect':
            request.session['isconnected'] = 0
        if client_ip in socket_dic:
            socket = socket_dic[client_ip]
            socket.send(data)
    return HttpResponse(json.dumps({'status': 0}))
