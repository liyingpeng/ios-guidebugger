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
import socket
import json

import helpers.lldbviewhelper as viewhelp


class SocketCommunity(object):
    """
    Class deal with socket community
    """

    def __init__(self):
        self.lldb_sock = None
        self.port = 8089
        self.ip = socket.gethostbyname(socket.gethostname())
        self.dispatcher = CommandDispatcher()

    def socket_recv(self):
        """
        Receive data from socket server constantly
        """
        self.lldb_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lldb_sock.connect((self.ip, self.port))

        while True:
            info = self.lldb_sock.recv(1024)
            if info:
                dataInfo = json.loads(info)
                command = dataInfo["command"]
                if command == 'disconnect':
                    break
                else:
                    self.dispatcher.dispatch_command(command, dataInfo)


class CommandDispatcher(object):
    """
    Class dispatch command
    """

    def __init__(self):
        super(CommandDispatcher, self).__init__()
        self.displaySetting = viewhelp.DisplaySetting()

    def dispatch_command(self, commandName, dataInfo):
        """
        Dispatch command

        Args:
            commandName: command name to dispatch
            dataInfo: the data should be carry
        """
        dispatcher = {
            'changeFrame': self._changeframe_command,
            'addBorder': self._addborder_command,
        }
        deal_fun = dispatcher.get(commandName)
        return deal_fun(dataInfo)

    def _changeframe_command(self, dataInfo):
        data = dataInfo['data']
        self.displaySetting.setViewFrameWeb(str(data['address']), data)

    def _addborder_command(self, dataInfo):
        address = dataInfo['address'].encode('utf-8')
        self.displaySetting.setViewBorder(address)
