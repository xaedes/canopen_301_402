#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from funcy import partial

from canopen_301_402.constants import *

from canopen_301_402.canopen_301.state import Can301State
from canopen_301_402.canopen_301.obj_dict import CanOpenObjectDictionary
from canopen_301_402.canopen_402.state import Can402State

from canopen_301_402.canopen_301.nmt import CanOpenNetworkManagement
from canopen_301_402.canopen_301.sdo import CanOpenSdoTransfer
from canopen_301_402.canopen_301.pdo import CanOpenPdoTransfer
from canopen_301_402.canopen_301.connection_set import ConnectionSet

# class CanOpenNodeClient(object):
#     """docstring for CanOpenNodeClient"""
#     def __init__(self, node):
#         super(CanOpenNodeClient, self).__init__()
#         self.node = node
#         self.canopen = node.canopen
        

class CanOpenNode(object):
    def __init__(self, canopen, node_id, eds_filename=None):
        super(CanOpenNode, self).__init__()
        self.canopen = canopen
        self.node_id = node_id

        # load eds file containing application specific profile
        self.eds = EdsFile()
        if eds_filename is not None:
            self.eds.read(eds_filename)

        # set up predefined connection set, mapping canopen services to function codes
        self.connection_set = ConnectionSet()
        self.connection_set.setup_from_eds(self.eds)

        # initialize services
        self.nmt = CanOpenNetworkManagement(self)
        self.sdo = CanOpenSdoTransfer(self)
        self.pdo = CanOpenPdoTransfer(self)

        # object dictionary
        self.obj_dict = CanOpenObjectDictionary(self.canopen)

        self.state301 = Can301State.initialisation
        
        self.state402 = Can402State.switch_on_disabled


        # self.client = CanOpenNodeClient(self)
        # todo self.master = CanOpenNodeMaster(self) 

        self.can402_supported = None # None means unknown, otherwise it is Boolean
        self.check_402()
        
        # setup routing to services
        self.services = dict()
        self.services[CanOpenService.nmt] = self.nmt.process_msg
        self.services[CanOpenService.nmt_error_control] = self.nmt.process_msg
        self.services[CanOpenService.sdo_tx] = self.sdo.process_msg
        self.services[CanOpenService.sdo_rx] = self.sdo.process_msg
        self.services[CanOpenService.pdo1_tx] = self.pdo.process_msg
        self.services[CanOpenService.pdo1_rx] = self.pdo.process_msg
        self.services[CanOpenService.pdo2_tx] = self.pdo.process_msg
        self.services[CanOpenService.pdo2_rx] = self.pdo.process_msg
        self.services[CanOpenService.pdo3_tx] = self.pdo.process_msg
        self.services[CanOpenService.pdo3_rx] = self.pdo.process_msg
        self.services[CanOpenService.pdo4_tx] = self.pdo.process_msg
        self.services[CanOpenService.pdo4_rx] = self.pdo.process_msg
        self.services[CanOpenService.sync] = None # todo
        self.services[CanOpenService.emergency] = None # todo


    def send_nmt(self, command):
        '''
        @param command: Can301StateCommand
        '''
        self.canopen.nmt.send_nmt(command, self.node_id)

    def send_sdo_write_request(self, index, subindex, data, response_callback):
        self.canopen.sdo.send_sdo_write_request(self.node_id, index, subindex, data, response_callback)

    def send_sdo_read_request(self, index, subindex, response_callback):
        self.canopen.sdo.send_sdo_write_request(self.node_id, index, subindex, response_callback)

    def check_402(self):
        '''
        @summary: checks whether node has 402 capabilities
                  it does so by look for controlword on 0x6040.00 and status word on 0x6041.00
        
        '''

        def check_for_both():
            if ((self.obj_dict.objects[(self.controlword_index, self.controlword_subindex)].value is None)
                or (self.obj_dict.objects[(self.statusword_index, self.statusword_subindex)].value is None)):
                self.can402_supported = False
            elif ((type(self.obj_dict.objects[(self.controlword_index, self.controlword_subindex)].value) == int)
                or (type(self.obj_dict.objects[(self.statusword_index, self.statusword_subindex)].value) == int)):
                self.can402_supported = True
            # otherwise one response may not yet have arrived

        def response(index, subindex, error,data=None):
            if error is None:
                datatype = self.obj_dict.objects[(index, subindex)].datatype
                if datatype is None:
                    # datatype not set?
                    raise RuntimeError()
                self.obj_dict.objects[(index, subindex)].value = datatype.decode(data)
            else:
                self.obj_dict.objects[(index, subindex)].value = None
            check_for_both()
                

        self.send_sdo_read_request(self.controlword_index, self.controlword_subindex, 
                                    partial(response,self.controlword_index, self.controlword_subindex))
        self.send_sdo_read_request(self.statusword_index, self.statusword_subindex, 
                                    partial(response,self.statusword_index, self.statusword_subindex))

        # todo: add timeout that sets can402_supported to False


    def change_402_state(self, command):
        '''
        @param command: Can402StateCommand
        '''

        # get current state
        if not self.can402_supported:
            raise Exception()

        state = self.obj_dict.objects[Can402Objects.controlword]
        datatype = self.obj_dict.datatypes[Can402Objects.controlword]
        if state is None: 
            raise Exception()

        assert datatype.identifier() == CanOpenBasicDatatypes.uint16

        def response(new_state,error):
            if error is None: # success
                pass # todo: change state
                self.obj_dict.objects[Can402Objects.controlword] = new_state
            else:
                print error # todo: replace by some kind of logger

        # todo: make this dynamic, maybe load from eds?
        bits = Can402StateCommandBits[command] # value of bits to be replaced
        mask = Can402StateCommandMask[command] # which bits shall be replaced
        # set all bits to zero that will be replaced 
        state = state & (~mask & 0xFFFF)
        # replace bits
        state = state | (mask & bits & 0xFFFF)
        data = [state & 0xFF, (state >> 8) & 0xFF]

        self.send_sdo_write_request(index, subindex, data, partial(response,new_state=state))
