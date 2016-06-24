#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import threading

from canopen_301_402.canopen_msgs.msgs import *
from canopen_301_402.constants import *

class AsyncOperation(object):
    """docstring for AsyncOperation"""
    def __init__(self, node, timeout=None):
        super(AsyncOperation, self).__init__()
        self.node = node
        self.canopen = node.canopen
        self.timeout = timeout
        self.timeout_timer = None


        self.evt_done = threading.Event()
        self.evt_success = threading.Event()
        self.evt_timeout = threading.Event()
        self.evt_fault = threading.Event()

    def _on_timeout(self):
        self.evt_timeout.set()
        self.evt_done.set()

    def start(self):
        if self.timeout is not None:
            self.timeout_timer = threading.Timer(self.timeout, self._on_timeout)
            self.timeout_timer.start()
        else:
            self.timeout_timer = None

        self.node.current_operations.append(self)
        self.do()

    def do(self):
        pass
        
    def process_msg(self, msg):
        return False

    def _on_done(self):
        if self in self.node.current_operations:
            try:
                self.node.current_operations.remove(self)
            except:
                pass

    def on_success(self):
        self.evt_success.set()
        self.evt_done.set()
        self._on_done()
        
    def on_fault(self):
        self.evt_fault.set()
        self.evt_done.set()
        self._on_done()
        
    def on_timeout(self):
        self.evt_timeout.set()
        self.evt_done.set()
        self._on_done()






