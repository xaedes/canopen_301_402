#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from canopen_301_402.constants import *
from canopen_301_402.async.sdo_write import SdoWrite

class ChangeControlword(SdoWrite):
    """docstring for Set402Mode"""
    def __init__(self, node, updates, *args, **kwargs):
        self.node = node
        self.updates = updates

        index, subindex = Can402Objects.controlword

        self.controlword = self.node.controlword

        for key, value in self.updates.iteritems():
            if value:
                self.controlword |= (1 << key.value)
            else:
                self.controlword &= ~(1 << key.value)
                
        data = [self.controlword & 0xFF, (self.controlword >> 8) & 0xFF]


        super(ChangeControlword, self).__init__(node, index, subindex, data, *args, **kwargs)

