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
import lldb

import lldbbase as base


class DisplaySetting(object):
    """
    Class provide funstions for Command change view property dynamically
    """

    def __init__(self):
        super(DisplaySetting, self).__init__()
        self.functionalView = _FunctionalView()
        self.lastModify = None

    def _flushCoreAnimationTransaction(self):
        lldb.debugger.HandleCommand('p (void)[CATransaction flush]')

    def setViewFrameWeb(self, object, framedata):
        """
        change view frame dynamically

        Args:
            object: memory address in device
            framedata: dict value for frame data
        """
        frameExp = '(CGRect){{%s, %s}, {%s, %s}}' % (str(framedata['left']),
                                                     str(framedata['top']),
                                                     str(framedata['width']),
                                                     str(framedata['height']))
        lldb.debugger.HandleCommand(
            'p (void)[' + object + ' setFrame:%s' % frameExp + ']')
        self._flushCoreAnimationTransaction()

    def setViewBorder(self, obj):
        """
        Add border for a single view

        Args:
            obj: memory address in device for the view
        """

        def _setBorder(layer, width, color, colorClass):
            lldb.debugger.HandleCommand(
                'p (void)[%s setBorderWidth:(CGFloat)%s]' % (layer, width))
            lldb.debugger.HandleCommand(
                'p (void)[%s setBorderColor:(CGColorRef)[(id)[%s %sColor] CGColor]]' % (layer, colorClass, color))

        if self.lastModify:
            self.unBorderedView()
        depth = 0
        if self.functionalView.isView(obj):
            prevLevel = 0
            for view, level in self.functionalView.subviewsOfView(obj):
                if level > depth:
                    break
                if prevLevel != level:
                    prevLevel = level
                layer = self.functionalView.convertToLayer(view)
                _setBorder(layer, 2.0, "red", 'UIColor')
                self.lastModify = obj
        else:
            # `obj` is not a view, make sure recursive bordering is not requested
            assert depth <= 0, "Recursive bordering is only supported for UIViews or NSViews"
            layer = self.functionalView.convertToLayer(obj)
            _setBorder(layer, 2.0, "red", 'UIColor')
            self.lastModify = obj

        lldb.debugger.HandleCommand('caflush')

    def unBorderedView(self):
        """
        Unborder for a single view

        Args:
            obj: memory address in device for the view
        """
        def _setUnborder(layer):
            lldb.debugger.HandleCommand(
                'eobjc (void)[%s setBorderWidth:(CGFloat)%s]' % (layer, 0))

        obj = self.lastModify
        depth = 0
        if self.functionalView.isView(obj):
            for view, level in self.functionalView.subviewsOfView(obj):
                if level > depth:
                    break
                layer = self.functionalView.convertToLayer(view)
                _setUnborder(layer)
        else:
            # `obj` is not a view, make sure recursive unbordering is not requested
            assert depth <= 0, "Recursive unbordering is only supported for UIViews or NSViews"
            layer = self.functionalView.convertToLayer(obj)
            _setUnborder(layer)

        self._flushCoreAnimationTransaction()


class _FunctionalView(object):
    """
    Class provide funstions for DisplaySetting instance change view property dynamically
    """

    def __init__(self):
        super(_FunctionalView, self).__init__()

    def _isUIView(self, obj):
        return base.evaluateBooleanExpression('[(id)%s isKindOfClass:(Class)[UIView class]]' % obj)

    def isView(self, obj):
        """
        Judge the obj is a NSView or UIView
        """
        return self._isUIView(obj)

    def subviewsOfView(self, view):
        """
        Generates a BFS of the views tree starting at the given view as root.
        Yields a tuple of the current view in the tree and its level (view, level)
        """
        views = [(view, 0)]
        yield views[0]
        while views:
            (view, level) = views.pop(0)
            subviews = base.evaluateExpression('(id)[%s subviews]' % view)
            subviewsCount = int(base.evaluateExpression(
                '(int)[(id)%s count]' % subviews))
            for i in xrange(subviewsCount):
                subview = base.evaluateExpression(
                    '(id)[%s objectAtIndex:%i]' % (subviews, i))
                views.append((subview, level + 1))
                yield (subview, level + 1)

    def convertToLayer(self, viewOrLayer):
        """
        Convert the View or layer to a CALayer
        """
        expression_cla = '[(id)%s isKindOfClass:(Class)[CALayer class]]' % viewOrLayer
        expression_sel = '[(id)%s respondsToSelector:(SEL)@selector(layer)]' % viewOrLayer
        if base.evaluateBooleanExpression(expression_cla):
            return viewOrLayer
        elif base.evaluateBooleanExpression(expression_sel):
            return base.evaluateExpression('(CALayer *)[%s layer]' % viewOrLayer)
        else:
            raise Exception('Argument must be a CALayer, UIView, or NSView.')

if __name__ == '__main__':
    pass
