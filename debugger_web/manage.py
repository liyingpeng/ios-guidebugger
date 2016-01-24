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
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "debugger_web.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
