#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from collections import defaultdict
from funcy import partial

import can

from canopen_301_402.constants import *
from canopen_301_402.signal import Signal
from canopen_301_402.assertions import Assertions
from canopen_301_402.canopen_301.msg import CanOpenMessage
from canopen_301_402.canopen_301.service import CanOpenServiceBaseClass

class SdoReadRequest(object):
    """docstring for SdoReadRequest"""
    def __init__(self, sdo, node_id, index, subindex):
        Assertions.assert_node_id(node_id)
        Assertions.assert_index(index)
        Assertions.assert_subindex(subindex)
        super(SdoReadRequest, self).__init__()
        self.sdo = sdo
        self.canopen = sdo.canopen
        self.node_id = node_id
        self.index = index
        self.subindex = subindex

        self.signal_success = Signal()
        self.signal_error = Signal()

    def _on_success(self, data):
        self.signal_success.dispatch(self, data)

    def _on_error(self, error):
        self.signal_error.dispatch(self, error)

class SdoWriteRequest(object):
    """docstring for SdoWriteRequest"""
    def __init__(self, sdo, node_id, index, subindex, data):
        Assertions.assert_node_id(node_id)
        Assertions.assert_index(index)
        Assertions.assert_subindex(subindex)
        Assertions.assert_data(data,maximum_len=4)
        super(SdoReadRequest, self).__init__()
        self.sdo = sdo
        self.canopen = sdo.canopen
        self.node_id = node_id
        self.index = index
        self.subindex = subindex
        self.data = data

        self.signal_success = Signal()
        self.signal_error = Signal()



    def _on_success(self):
        self.signal_success.dispatch(self, self.data)

    def _on_error(self, error):
        self.signal_error.dispatch(self, error)


class CanOpenSdoTransfer(CanOpenServiceBaseClass):
    '''
    @summary: for use as cooperative base class in CanOpen
    '''
    def __init__(self, *args, **kwargs):
        super(CanOpenSdoTransfer, self).__init__(*args, **kwargs)
        self.response_callbacks = dict()
        self.signals_error = defaultdict(Signal)
        self.signals_read_success = defaultdict(Signal)
        self.signals_write_success = defaultdict(Signal)

        self.pending_operations = list()
        self.write_requests = defaultdict(list)
        self.read_requests = defaultdict(list)

    def send_sdo_write_request(self, node_id, index, subindex, data, response_callback):
        '''
        @summary: 
        @param node_id:
        @param index:
        @param subindex:
        @param data: byte array, maximum length: 4 bytes
        @param response_callback: function(error), where error is None if sucessful or string containing error description
        @result: 
        '''
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
        
        data = ([sdo_download_request, # specifies, that we want to write value to object dictionary
                (index & 0xff),       # index low byte
                (index>>8),           # index high byte
                subindex]             # 8 bit subindex
                + data)                # data to be written

        # register callbacks to sdo response
        self.signals_write_success[(node_id,index,subindex)].register_once(partial(response,error=None))
        self.signals_error[(node_id,index,subindex)].register_once(response_callback)
        
        # send canopen message
        service = CanOpenService.sdo_rx
        function_code = self.canopen.connection_set.determine_function_code(service)
        msg = CanOpenMessage(function_code,node_id,service,data)

        self.canopen.send_msg(msg)


    def send_sdo_read_request(self, node_id, index, subindex, response_callback):
        '''
        @summary: 
        @param node_id:
        @param index:
        @param subindex:
        @param response_callback: function(error,[byte]: data=none), where error is None or string containing error description
        @result: 
        '''
        Assertions.assert_node_id(node_id)
        Assertions.assert_index(index)
        Assertions.assert_subindex(subindex)

        data = [CanData.sdo_upload_request, # specifies, that we want to read value from object dictionary
                (index & 0xff),             # index low byte
                (index >> 8),               # index high byte
                subindex]                   # 8 bit subindex

        # register callbacks to sdo response
        self.signals_read_success[(index,subindex)].register_once(partial(response,error=None))
        self.signals_error[(index,subindex)].register_once(response_callback)

        # send canopen message
        service = CanOpenService.sdo_rx
        function_code = self.canopen.connection_set.determine_function_code(service)
        msg = CanOpenMessage(function_code,node_id,service,data)

        self.canopen.send_msg(msg)


    def process_msg(self, msg):
        # convert msg into sdo msg



        # sdo response
        if msg.service == CanOpenService.sdo_tx: 
            
            # todo replace with softer error
            assert len(msg.data) == 8

            index = msg.data[1] | (msg.data[2] << 8)
            subindex = msg.data[3]
            node_id = msg.node_id

            # sdo error
            if msg.data[0] == CanData.sdo_error:
                # error code is in little endian 
                error = msg.data[4] | (msg.data[5]<<8) | (msg.data[6]<<16) | (msg.data[7]<<24)
                if error_msg in CanErrors:
                    error_msg = CanErrors[error]
                else:
                    error_msg = CanErrors.unknown % hex(error)

                self.signals_error[(node_id,index,subindex)].dispatch(error=error_msg)

            # read response
            if (msg.data[0] & CanData.sdo_upload_response) == CanData.sdo_upload_response:
                # len_response_data of sdo object is encoded as this:
                # msg.data[0] == CanData.sdo_upload_response | ((4-len_response_data)<<2)
                len_response_data = 4-(msg.data[0] >> 2) & 0b11
                data = msg.data[4:4+len_response_data]

                self.signals_read_success[(node_id,index,subindex)].dispatch(data=data)


            # write response: success
            if msg.data[0] == CanData.sdo_download_response: 
                # get index and subindex from msg

                self.signals_write_success[(node_id,index,subindex)].dispatch()
