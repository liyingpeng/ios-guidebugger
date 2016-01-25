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
import requests
import socket

# baseUrl = 'http://dbl-cidapp-1.epc.baidu.com:8086'
baseUrl = 'http://' + socket.gethostbyname(socket.gethostname()) + ':' + '8086'


def send_buildconnet_request(url):
    """
    send http request to build socket connet
    """
    requests.get(baseUrl + url)


def sendRequest(url, param, callback):
    """
    send basic http request to django server
    """
    requests.post(baseUrl + url, param)
    callback()
