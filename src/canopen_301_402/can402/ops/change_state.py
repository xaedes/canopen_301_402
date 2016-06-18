#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from canopen_301_402.constants import *
from canopen_301_402.async.sdo_write import SdoWrite


class ChangeState(SdoWrite):
    """docstring for ChangeState"""
    def __init__(self, node, command, *args, **kwargs):
        self.node = node
        self.command = command

        if self.node.state402 not in Can402StateTransitions: raise Exception()
        if command not in Can402StateTransitions[self.node.state402]: raise ValueError()
        self.new_state = Can402StateTransitions[self.node.state402][command]
        
        index, subindex = Can402Objects.controlword

        self.controlword = self.node.controlword

        bits = Can402StateCommandBits[command] # value of bits to be replaced
        mask = Can402StateCommandMask[command] # which bits shall be replaced
        # set all bits to zero that will be replaced 
        self.controlword = self.controlword & (~mask & 0xFFFF)
        # replace bits
        self.controlword = self.controlword | (mask & bits & 0xFFFF)
        data = [self.controlword & 0xFF, (self.controlword >> 8) & 0xFF]

        super(ChangeState, self).__init__(node, index, subindex, data, *args, **kwargs)
        
    def do(self):
        super(ChangeState, self).do()

    def on_success(self):
        self.node.state402 = self.new_state
        self.node.controlword = self.controlword

        super(ChangeState, self).on_success()


