#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from collections import defaultdict

import can

from canopen_301_402.constants import *
from canopen_301_402.utils import *
from canopen_301_402.assertions import Assertions
from canopen_301_402.node import CanOpenNode
from canopen_301_402.canopen_301.cob import CanOpenId
from canopen_301_402.canopen_301.broadcast import CanOpenBroadcast
from canopen_301_402.canopen_msgs.msg import CanOpenMessage
from canopen_301_402.canopen_msgs.msgs import *
from canopen_301_402.canopen_301.datatypes import CanDatatypes
from canopen_301_402.canopen_301.connection_set import ConnectionSet

TRACE = True

if TRACE:
    import hunter
    hunter.trace(module_contains="canopen_301_402")



eds_config = defaultdict(lambda:None,{
    1: "/home/xaedes/gits/fahrrad/eds/605.3150.68-A-EK-2-60.eds"
})

class CanOpen(can.Listener):
    """docstring for CanOpen"""
    def __init__(self, bus, eds_config):
        super(CanOpen, self).__init__()
        self.bus = bus
        self.notifier = can.Notifier(self.bus,[self])

        self.eds_config = eds_config

        self.msgs = CanOpenMessages(self)

        # canopen datatypes
        self.datatypes = CanDatatypes()

        # canopen nodes
        self.nodes = defaultdict(lambda:None)
        self.nodes[0] = CanOpenBroadcast(self)

        # set up predefined connection set, mapping canopen services to function codes
        self.connection_set = ConnectionSet()

        self.collect_messages = True
        self.collected_messages = list()

    def get_node(self, node_id):
        if self.nodes[node_id] is None:
            self.nodes[node_id] = self.init_node(node_id)

        return self.nodes[node_id]

    def init_node(self, node_id):
        return CanOpenNode(self, node_id, self.eds_config[node_id])

    def get_connection_set(self, node_id):
        if node_id == 0: 
            # for broadcast messages (node_id==0) use default connection_set
            return self.connection_set
            
        node = self.get_node(node_id)
        return node.connection_set

    def send_can(self, can_id, data):
        '''
        @summary: send message with data to 11 bit can_id 
        @param bus: can.Bus
        @param can_id: CanID (11bit)
        @param data: [byte] 0 <= len(data) <= 4
        @deprecated: use self.send_msg
        @result: 
        '''
        Assertions.assert_data(data)
        Assertions.assert_can_id(can_id)
        msg = can.Message(arbitration_id=can_id,data=data,extended_id=False)
        self.bus.send(msg)

    def send_msg(self, msg):
        '''
        @summary: 
        @param msg: CanOpenMessage or subclass
        @result: 
        '''
        self.on_message_received(msg)

        self.bus.send(msg.to_can_msg())


        # print msg.__dict__

        # # route canopen message to responsible service
        # node = self.get_node(msg.node_id)
        # service = node.services[msg.service]

        # print "service",service
        # if service is not None:
        #     service.process_msg(msg)


    def on_message_received(self, msg):
        if TRACE:
            hunter.trace(module_contains="canopen_301_402")

        print "on_message_received"
        # print "--"
        # print "raw", msg


        # convert message to canopen message
        if type(msg) == can.Message:
            msg = CanOpenMessage.from_can_msg(msg, self)

        # parse message into higher level canopen message types
        if type(msg) == CanOpenMessage:
            msg = self.msgs.try_to_upgrage_canopen_message(msg)

        print can_msg_to_str(msg.to_can_msg())

        if self.collect_messages:
            self.collected_messages.append(msg)

        # print "msg type: ", type(msg)
        # print msg.__dict__
        # print ""
        
        # route canopen message to responsible service
        if msg.broadcast:
            for node in self.nodes.itervalues():
                service = node.services[msg.service]
                if service is not None:
                    service.process_msg(msg)
        else:
            
            node = self.get_node(msg.node_id)
            service = node.services[msg.service]

            # print "service",service
            if service is not None:
                service.process_msg(msg)

        # print ""
        # print ""
        # print ""

    def start_remote_nodes(self):
        msg = CanOpenMessageNmtCommand(self,node_id=0,command=Can301StateCommand.start_remote_node)
        self.send_msg(msg)

