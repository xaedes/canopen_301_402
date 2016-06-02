#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import can

from canopen_301_402.canopen_301.cob import CanOpenId

class CanOpenMessage(object):
    def __init__(self, function_code, node_id, service, data):
        '''
        @summary: Represents a higher level interpretation of a regular can message
        @param function_code: 4 bit opencan function code
        @param node_id: 7 bit node_id
        '''

        super(CanOpenMessage, self).__init__()
        self.function_code = function_code
        self.node_id = node_id
        self.service = service
        self.data = data
        
    def to_can_msg(self):
        arbitration_id = CanOpenId.encode(self.function_code, self.node_id)
        can.Message(arbitration_id=arbitration_id,data=data,extended_id=False)

    @classmethod
    def from_can_msg(cls, msg, connection_set):
        assert msg.extended_id == False 

        function_code, node_id = CanOpenId.decode(msg.arbitration_id)
        service = connection_set.determine_service(function_code, node_id)
        return CanOpenMessage(function_code,node_id,service,msg.data)
        