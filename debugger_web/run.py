#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This module provide configure file management service in i18n environment.

Authors: liyingpeng(liyingpeng@baidu.com)
Date:    2016/01/20 17:23:06
"""
import os
import socket

port = '8086'
local_ip = socket.gethostbyname(socket.gethostname())

os.system('python manage.py runserver ' + local_ip + ':' + port)
