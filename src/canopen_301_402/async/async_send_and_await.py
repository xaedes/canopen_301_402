#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from canopen_301_402.async.async_operation import AsyncOperation

class AsyncSendAndAwait(AsyncOperation):
    """docstring for AsyncChain"""
    def __init__(self, node, send_msg_factory, await_msg_predicate, *args, **kwargs):
        self.node = node
        self.send_msg_factory = send_msg_factory
        self.await_msg_predicate = await_msg_predicate
        super(AsyncSendAndAwait, self).__init__(node, *args, **kwargs)

    def do(self):
        msg = self.send_msg_factory()
        self.canopen.send(msg)

    def process_msg(self, msg):
        if self.await_msg_predicate(msg):
            self.on_success()
