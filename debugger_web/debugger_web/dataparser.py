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
import re
import json


class DataParser(object):
    """
    Class parse the data got from the server
    """

    def __init__(self):
        super(DataParser, self).__init__()

    def parsedata(self, data):
        """
        Parse the data to a formatted json stucture

        Returns:
            json data
        """
        stack = _Stack()
        datalist = data.split('\n')
        current_hierarchy = 0
        stack.push([])
        for i, dataItem in enumerate(datalist):
            hierarchy = len(re.findall(r'\s*\|\s*', dataItem))
            framedata = self._parsedata_item(dataItem)
            datainfo = framedata.__dict__
            if hierarchy == current_hierarchy:
                stack.top().append(datainfo)
            else:
                if hierarchy > current_hierarchy:
                    stack.push([])
                    stack.top().append(datainfo)
                else:
                    gap = current_hierarchy - hierarchy
                    while gap > 0:
                        popElement = stack.pop()
                        topElement = stack.top()
                        topElement.append(popElement)
                        if gap == 1:
                            topElement.append(datainfo)
                        gap -= 1
                current_hierarchy = hierarchy
        result = json.dumps(stack.merge())
        print result
        return result

    def _parsedata_item(self, dataItem):
        """
        Parse the dataitem to a FrameData instance
        Returns:
            A FrameData instance
        """
        def _preprocessing(info):
            if info.startswith('<'):
                info = info[1:]
            elif info.endswith('>'):
                info = info[: -1]
            return info

        formatdata_item = re.sub(r'\s*\|\s*', r'', dataItem).strip()
        framedata = _FrameData()

        address_keyvalue = re.findall(
            r'[^:;=]*[:]\s0x[0-9a-zA-Z]+', formatdata_item)[0]
        pare = re.split(r':', _preprocessing(address_keyvalue))
        framedata.type = pare[0].strip(' ;')
        framedata.address = pare[1].strip(' ;')

        propertygroup = re.findall(r'[^;:=]+[=][^=]+[;>]', formatdata_item)
        for i, propertyInfo in enumerate(propertygroup):
            propertyInfo = _preprocessing(propertyInfo)

            keyValue = re.split(r'=', propertyInfo)
            if len(keyValue) > 1:
                propertyName = keyValue[0].strip(' ;')
                propertyValue = keyValue[1].strip(' ;')
                if propertyName == 'frame':
                    framelist = re.findall(r'[0-9.]+', propertyValue)
                    framedata.left = framelist[0]
                    framedata.top = framelist[1]
                    framedata.width = framelist[2]
                    framedata.height = framelist[3]
                else:
                    setattr(framedata, propertyName, propertyValue)

        return framedata


class _FrameData(object):

    def __init__(self):
        super(_FrameData, self).__init__()


class _Stack(object):
    """
    Stack stucture
    """

    def __init__(self):
        super(_Stack, self).__init__()
        self.stack = []

    def empty(self):
        """
        Return is the stack empty
        """
        return self.stack == []

    def push(self, data):
        """
        Push an object to statck
        """
        self.stack.append(data)

    def pop(self):
        """
        Pop an obj from stack
        """
        if self.empty():
            return None
        else:
            return self.stack.pop(-1)

    def merge(self):
        """
        Merge the remain object to a list
        """
        if self.empty():
            return None
        else:
            while self.top():
                popElement = self.pop()
                topElement = self.top()
                if topElement:
                    topElement.append(popElement)
                else:
                    return popElement

    def top(self):
        """
        Return top element of the stack
        """
        if self.empty():
            return None
        else:
            return self.stack[-1]

    def length(self):
        """
        Return the length of stack
        """
        return len(self.stack)
