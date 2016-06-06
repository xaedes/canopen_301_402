#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import can

from canopen_301_402.constants import *
from canopen_301_402.canopen_301.cob import CanOpenId

class CanOpenMessage(object):
    def __init__(self, function_code, node_id, service, data, msg_type = CanOpenMessageType.not_specified):
        '''
        @summary: Represents a higher level interpretation of a regular can message
        
        @param function_code: 4 bit opencan function code
        @param node_id:       7 bit node_id
        @param service:       CanOpenService
        @param data:          byte array [maximum length 8]
        @param msg_type:      CanOpenMessageType

        '''

        super(CanOpenMessage, self).__init__()
        self.msg_type = msg_type
        self.function_code = function_code
        self.node_id = node_id
        self.service = service
        if self.service in [CanOpenService.nmt,CanOpenService.sync]:
            self.broadcast = True
        self.data = data
        
    def to_can_msg(self):
        if self.broadcast:
            arbitration_id = CanOpenId.encode(self.function_code, 0)
        else:
            arbitration_id = CanOpenId.encode(self.function_code, self.node_id)
            
        return can.Message(arbitration_id=arbitration_id,data=self.data,extended_id=False)

    @classmethod
    def from_can_msg(cls, msg, canopen):
        assert not hasattr(msg,"extended_id") or (msg.extended_id == False) 

        function_code, node_id = CanOpenId.decode(msg.arbitration_id)

        connection_set = canopen.get_connection_set(node_id)

        service = connection_set.determine_service(function_code, node_id)

        return CanOpenMessage(function_code,node_id,service,msg.data)
        
