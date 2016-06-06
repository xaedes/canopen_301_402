#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from collections import defaultdict

import can

from canopen_301_402.constants import *
from canopen_301_402.assertions import Assertions
from canopen_301_402.node import CanOpenNode
from canopen_301_402.canopen_301.eds import *
from canopen_301_402.canopen_301.cob import CanOpenId
from canopen_301_402.canopen_301.broadcast import CanOpenBroadcast
from canopen_301_402.canopen_301.msg import CanOpenMessage
from canopen_301_402.canopen_301.msgs import Messages
from canopen_301_402.canopen_301.datatypes import CanDatatypes
from canopen_301_402.canopen_301.connection_set import ConnectionSet


eds_config = defaultdict(lambda:None,{
    1: "path/to/file.eds"
})

class CanOpen(can.Listener):
    """docstring for CanOpen"""
    def __init__(self, bus, eds_config):
        super(CanOpen, self).__init__()
        self.bus = bus
        self.notifier = can.Notifier(self.bus,[self])

        self.eds_config = eds_config

        self.msgs = Messages(self)

        # canopen datatypes
        self.datatypes = CanDatatypes()

        # canopen nodes
        self.nodes = defaultdict(lambda:None)
        self.nodes[0] = CanOpenBroadcast(self)

        # set up predefined connection set, mapping canopen services to function codes
        self.connection_set = ConnectionSet()

    def get_node(self, node_id):
        if self.nodes[node_id] is None:
            self.nodes[node_id] = self.init_node(node_id)

        return self.nodes[node_id]

    def init_node(self, node_id):
        return CanOpenNode(self, node_id, self.eds_config[msg.node_id])

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

    def send_msg(self, can_open_msg):
        '''
        @summary: 
        @param can_open_msg: CanOpenMessage
        @result: 
        '''
        self.bus.send(can_open_msg.to_can_msg())


    def on_message_received(self, msg):
        print msg

        # convert message to canopen message
        msg = CanOpenMessage.from_can_msg(msg, self)

        # route canopen message to responsible service
        node = self.get_node(msg.node_id)
        service = node.services[msg.service]

        assert callable(service)
        service(msg)

    def start_remote_nodes(self):
        msg = self.msgs.nmt(node_id=0,command=Can301StateCommandBits.start_remote_node)
        self.send_msg(msg)
