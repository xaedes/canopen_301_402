#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import can

from canopen_301_402.utils import *
from canopen_301_402.connection_set import ConnectionSet
from canopen_301_402.canopen_msgs.msg import CanOpenMessage
from canopen_301_402.canopen_msgs.msgs import *

import Queue

from collections import defaultdict

TRACE = True

if TRACE:
    import hunter
    hunter.trace(module_contains="canopen_301_402")


class CanOpen(can.Listener):
    """docstring for CanOpen"""
    def __init__(self, bus):
        super(CanOpen, self).__init__()
        self.bus = bus
        self.notifier = can.Notifier(self.bus,[self])

        self.connection_set = ConnectionSet()

        self.msgs = CanOpenMessages(self)

        self.msg_queues = defaultdict(Queue.Queue)

        self.msg_history = list()
        self.enable_history = True

    def send(self, msg):
        # send can msg
        if isinstance(msg, CanOpenMessage):
            self.bus.send(msg.to_can_msg())
        elif type(msg) == can.Message:
            self.bus.send(msg)
        elif type(msg) == str:
            self.bus.send(str_to_can_msg(msg))

        else:
            raise ValueError()


    def on_message_received(self, msg):
        hunter.trace(module_contains="canopen_301_402")

        # convert message to canopen message
        if type(msg) == can.Message:
            msg = CanOpenMessage.from_can_msg(msg, self)

        # parse message into higher level canopen message types
        if type(msg) == CanOpenMessage:
            msg = self.msgs.try_to_upgrage_canopen_message(msg)

        print "---"
        print type(msg), msg
        print msg.__dict__
        print ""

        # history
        if self.enable_history:
            self.msg_history.append(msg)

        # enqueue CanOpenMessage
        self.msg_queues[msg.node_id].put(msg)
