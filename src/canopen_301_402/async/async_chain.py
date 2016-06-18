#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from canopen_301_402.async.async_operation import AsyncOperation

class AsyncChain(AsyncOperation):
    """docstring for AsyncChain"""
    def __init__(self, node, operations, *args, **kwargs):
        self.node = node
        self.operations = operations

        super(AsyncChain, self).__init__(node, *args, **kwargs)

    def do(self):
        for Op in self.operations:
            op = Op()
            op.start()
            op.evt_done.wait()
            if op.evt_success.isSet():
                continue
            elif op.evt_timeout.isSet():
                self.on_timeout()
                return
            elif op.evt_fault.isSet():
                self.on_fault()
                return
        self.on_success()
