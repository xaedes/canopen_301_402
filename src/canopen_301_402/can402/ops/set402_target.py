#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from funcy import partial

from canopen_301_402.constants import *
from canopen_301_402.async.async_chain import AsyncChain
from canopen_301_402.async.sdo_write import SdoWrite
from canopen_301_402.can402.ops.notify402_new_target import Notify402NewTarget



class Set402Target(AsyncChain):
    """docstring for Init402"""
    def __init__(self, node, value, relative=False, immediatly=False, *args, **kwargs):
        self.node = node
        self.value = value
        self.relative = relative
        self.immediatly = immediatly

        set_target_position = partial(SdoWrite,
                                node = node, 
                                index = Can402Objects.target_position[0], 
                                subindex = Can402Objects.target_position[1], 
                                data = struct.pack("<i",self.value))
        notify_new_target   = partial(Notify402NewTarget,
                                node = node, 
                                relative = self.relative, 
                                immediatly = self.immediatly)



        operations = [set_target_position, notify_new_target]

        super(Set402Target, self).__init__(node, operations, *args, **kwargs)
        
