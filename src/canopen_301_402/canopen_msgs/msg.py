#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import can

from canopen_301_402.constants import *
from canopen_301_402.canopen_301.cob import CanOpenId

class CanOpenMessage(object):
    def __init__(self, function_code, node_id, service, data, request=False):
        '''
        @summary: Represents a higher level interpretation of a regular can message
        
        @param function_code: 4 bit opencan function code
        @param node_id:       7 bit node_id
        @param service:       CanOpenService
        @param data:          byte array [maximum length 8]

        '''

        super(CanOpenMessage, self).__init__()
        self._function_code = function_code
        self._node_id = node_id
        self._service = service
        if self._service in [CanOpenService.nmt,CanOpenService.sync]:
            self._broadcast = True
        else:
            self._broadcast = False
        self._data = data
        self._request = request

    @property
    def node_id(self):
        return self._node_id

    @property
    def request(self):
        return self._request
        
    @property
    def function_code(self):
        return self._function_code
        
    @property
    def broadcast(self):
        return self._broadcast

    @property
    def service(self):
        return self._service
    
    @property
    def data(self):
        return self._data
    
        
    def to_can_msg(self):
        if self.broadcast:
            arbitration_id = CanOpenId.encode(self.function_code, 0)
        else:
            arbitration_id = CanOpenId.encode(self.function_code, self.node_id)

        return can.Message(arbitration_id=arbitration_id,data=self.data,extended_id=False,is_remote_frame=self.is_remote_frame)

    @classmethod
    def from_can_msg(cls, msg, canopen):
        assert not hasattr(msg,"extended_id") or (msg.extended_id == False) 

        function_code, node_id = CanOpenId.decode(msg.arbitration_id)

        connection_set = canopen.get_connection_set(node_id)

        service = connection_set.determine_service(function_code, node_id)

        return CanOpenMessage(function_code,node_id,service,msg.data,request=msg.is_remote_frame)
        
