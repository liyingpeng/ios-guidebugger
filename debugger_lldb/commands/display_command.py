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
import webbrowser
import socket

import lldbbase as base
import httpserver.webcommunity_client as httpclient
import httpserver.webcommunity_socket as community


def lldbcommands():
    """
    return all functional class instance for lldb to load

    Returns:
        list: functional class instance list
    """
    return [
        PrintViewHierarchyWebCommand(),
    ]


class PrintViewHierarchyWebCommand(base.Command):
    """
    A single Command class inherit base.Command
    """

    def name(self):
        """
        return command represent name
        """
        return 'openbrowser'

    def description(self):
        """
        return command description
        """
        return 'Print the recursion description of <aView>. to a webbrowser page'

    def args(self):
        return [base.CommandArgument(arg='aView', type='UIView*/NSView*', help='The view to print the description of.', default='__keyWindow_dynamic__')]

    def options(self):
        """
        return command arguments list
        """
        return [
            base.CommandArgument(short='-u',
                                 long='--up',
                                 arg='upwards',
                                 boolean=True,
                                 default=False,
                                 help='Print only the hierarchy directly above the view'),
            base.CommandArgument(short='-d',
                                 long='--depth',
                                 arg='depth',
                                 type='int',
                                 default="0",
                                 help='Print only to a given depth. 0 indicates infinite depth.'),
        ]

    def run(self, arguments, options):
        """
        make run command

        Args:
            auguments: command arguments list
            options: command options
        """
        def _dealwithData(data):
            local_ip = socket.gethostbyname(socket.gethostname())
            params = {'viewdescription': data, "local_ip": local_ip}
            url = '/adddata'

            def _callback():
                chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
                webbrowser.get(chrome_path).open(httpclient.baseUrl + '/showdata')
                community.SocketCommunity().socket_recv()

            httpclient.sendRequest(url, params, _callback)

        if arguments[0] == '__keyWindow_dynamic__':
            arguments[0] = '(id)[[UIApplication sharedApplication] keyWindow]'

        printingMethod = 'recursiveDescription'

        description = base.evaluateExpressionValue(
            '(id)[' + arguments[0] + ' ' + printingMethod + ']').GetObjectDescription()

        if description:
            _dealwithData(description)
