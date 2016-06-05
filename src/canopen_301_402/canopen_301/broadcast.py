#!/usr/bin/env python2
# -*- coding: utf-8 -*-

class CanOpenBroadcast(object):
    """docstring for CanOpenBroadcast"""
    def __init__(self, canopen):
        super(CanOpenBroadcast, self).__init__()
        self.canopen = canopen
        
        # setup routing to services
        self.services = dict()
        self.services[CanOpenService.nmt] = self.nmt.process_msg
        self.services[CanOpenService.nmt_error_control] = self.nmt.process_msg
        self.services[CanOpenService.sync] = None # todo
        self.services[CanOpenService.emergency] = None # todo
