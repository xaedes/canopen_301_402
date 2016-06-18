#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from canopen_301_402.async.async_operation import AsyncOperation

class AsyncSend(AsyncOperation):
    """docstring for AsyncChain"""
    def __init__(self, node, send_msg_factory, *args, **kwargs):
        self.node = node
        self.send_msg_factory = send_msg_factory
        super(AsyncSend, self).__init__(node, *args, **kwargs)

    def do(self):
        msg = self.send_msg_factory()
        self.canopen.send(msg)
        self.on_success()
