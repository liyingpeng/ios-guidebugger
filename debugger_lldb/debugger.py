#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This module provide configure file management service in i18n environment.

Authors: liyingpeng(liyingpeng@baidu.com)
Date:    2016/01/20 17:23:06
"""
import os


filePath = os.path.realpath(__file__)
dirname = os.path.dirname(filePath)
userPath = os.path.expanduser('~')
filename = userPath + '/.lldbinit'
with open(filename, 'a') as f:
    realpath = 'command script import ' + dirname + '/lldbloadcommand.py' + '\n'
    print realpath
    f.write(realpath)
f.close()
