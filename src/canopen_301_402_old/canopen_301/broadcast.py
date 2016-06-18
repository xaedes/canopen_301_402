#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from canopen_301_402.constants import *

class CanOpenBroadcast(object):
    """docstring for CanOpenBroadcast"""
    def __init__(self, canopen):
        super(CanOpenBroadcast, self).__init__()
        self.canopen = canopen
        
        # setup routing to services
        self.services = dict()
        self.services[CanOpenService.nmt] = None
        self.services[CanOpenService.nmt_error_control] = None
        self.services[CanOpenService.sync] = None # todo
        self.services[CanOpenService.emergency] = None # todo
