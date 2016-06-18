#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from canopen_301_402.constants import *
from canopen_301_402.node import CanOpenNode

class Can402Node(CanOpenNode):
    """docstring for Can402Node"""
    def __init__(self, canopen, node_id):
        super(Can402Node, self).__init__(canopen, node_id)

        self.controlword = 0x0000
        self.statusword = 0x0000
        self.state402 = Can402State.switch_on_disabled

        self.receive_pdo1 = ReceivePdo1(self)
        self.receive_pdo1.start()
