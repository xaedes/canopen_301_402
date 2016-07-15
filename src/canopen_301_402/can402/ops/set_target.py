#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from funcy import partial

from canopen_301_402.constants import *
from canopen_301_402.async.async_chain import AsyncChain
from canopen_301_402.async.sdo_write_object import SdoWriteObject
from canopen_301_402.can402.ops.notify_new_target import NotifyNewTarget

import struct


class SetTarget(AsyncChain):
    """docstring for SetTarget"""
    def __init__(self, node, value, relative=False, immediatly=False, target_type="Position", *args, **kwargs):
        parameter_name = "Target " + target_type
        self.node = node
        self.value = value
        self.relative = relative
        self.immediatly = immediatly

        set_target = partial(SdoWriteObject,
                                node = node, 
                                parameter_name = parameter_name, 
                                value = self.value)
        notify_new_target   = partial(NotifyNewTarget,
                                node = node, 
                                relative = self.relative, 
                                immediatly = self.immediatly)



        operations = [set_target, notify_new_target]

        super(SetTarget, self).__init__(node, operations, *args, **kwargs)
        
