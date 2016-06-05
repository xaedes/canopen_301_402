#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from canopen_301_402.constants import *
from canopen_301_402.assertions import Assertions
from canopen_301_402.canopen_301.msg import CanOpenMessage

class Messages(object):
    """Message factory"""
    def __init__(self, canopen):
        super(Messages, self).__init__()
        self.canopen = canopen

    def nmt(self, node_id, command):
        '''
        @summary:  CanOpenMessage for nmt command
        @param cls:
        @param node_id: 0 = all nodes
        @param command: Can301StateCommand
        @result: 
        '''
        service = CanOpenService.nmt
        msg_type = CanOpenMessageType.nmt_command

        connection_set = self.canopen.get_connection_set(node_id)
        function_code = connection_set.determine_function_code(service)
        data = [Can301StateCommandBits[command], node_id]
        msg = CanOpenMessage(function_code, 0, service, data, msg_type)
        return msg
    
    def nmt_request(self):
        '''
        @summary: CanOpenMessage for nmt request  
        @param cls:
        @result: 
        '''
        node_id = 0
        service = CanOpenService.nmt
        msg_type = CanOpenMessageType.nmt_request

        connection_set = self.canopen.get_connection_set(node_id)
        function_code = connection_set.determine_function_code(service)
        
        data = []


        msg = CanOpenMessage(function_code, node_id, service, data, msg_type)
        return msg

    def sdo_write_request(self, node_id, index, subindex, data):
        Assertions.assert_node_id(node_id)
        Assertions.assert_index(index)
        Assertions.assert_subindex(subindex)
        Assertions.assert_data(data,maximum_len=4)

        len_data = len(data)

        if len_data == 0:
            # Falls keine Angabe der Anzahl Datenbytes erforderlich ist: Byte0 = 0x22
            sdo_download_request = CanData.sdo_download_request_bits - 1
        else:
            # encode number of data bytes to be written
            sdo_download_request = ((4-len_data)<<2) | CanData.sdo_download_request_bits
        
        data = [sdo_download_request, # specifies, that we want to write value to object dictionary
                (index & 0xff),       # index low byte
                (index>>8),           # index high byte
                subindex]             # 8 bit subindex
                + data           # data to be written
        
        # build canopen message
        service = CanOpenService.sdo_rx
        msg_type = CanOpenMessageType.sdo_write_request

        connection_set = self.canopen.get_connection_set(node_id)
        function_code = connection_set.determine_function_code(service)


        msg = CanOpenMessage(function_code, node_id, service, data, msg_type)
        return msg

    def sdo_read_request(self, node_id, index, subindex):
        Assertions.assert_node_id(node_id)
        Assertions.assert_index(index)
        Assertions.assert_subindex(subindex)


        data = [CanData.sdo_upload_request, # specifies, that we want to read value from object dictionary
                (index & 0xff),        # index low byte
                (index >> 8),          # index high byte
                subindex]              # 8 bit subindex


        # build canopen message
        service = CanOpenService.sdo_rx
        msg_type = CanOpenMessageType.sdo_read_request

        connection_set = self.canopen.get_connection_set(node_id)
        function_code = connection_set.determine_function_code(service)

        msg = CanOpenMessage(function_code, node_id, service, data, msg_type)
        return msg

