#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from collections import defaultdict
from funcy import partial

import can

from canopen_301_402.constants import *
from canopen_301_402.signal import Signal
from canopen_301_402.assertions import Assertions
from canopen_301_402.canopen_msgs.msg import CanOpenMessage
from canopen_301_402.canopen_msgs.msgs import *
from canopen_301_402.canopen_301.service import CanOpenServiceBaseClass

from flufl.enum import Enum

class SdoOperation(Enum):
    none = 0
    write_request = 1
    read_request = 2

class CanOpenSdoTransfer(CanOpenServiceBaseClass):
    '''
    @summary: for use as cooperative base class in CanOpen
    '''
    def __init__(self, *args, **kwargs):
        super(CanOpenSdoTransfer, self).__init__(*args, **kwargs)
        self.response_callbacks = dict()

        # maps from (index,subindex) to Signal:
        self.signal_error = defaultdict(Signal)
        self.signal_read_complete = defaultdict(Signal)
        self.signal_write_complete = defaultdict(Signal)

        self.pending_operation = SdoOperation.none
        self.pending_idx_subidx = None
        self.pending_write_data = None

    def process_msg(self, msg):

        if isinstance(msg, CanOpenMessageSdoReadRequest):
            self.pending_operation = SdoOperation.read_request
            self.pending_idx_subidx = msg.index, msg.subindex

        elif isinstance(msg, CanOpenMessageSdoWriteRequest):
            self.pending_operation = SdoOperation.write_request
            self.pending_idx_subidx = msg.index, msg.subindex
            self.pending_write_data = msg.write_data

        elif isinstance(msg, CanOpenMessageSdoReadResponse):
            if self.pending_operation == SdoOperation.read_request:
                self.signal_read_complete[self.pending_idx_subidx].dispatch(msg.read_data)
                self.pending_operation = SdoOperation.none
                self.pending_idx_subidx = None

        elif isinstance(msg, CanOpenMessageSdoWriteResponse):
            if self.pending_operation == SdoOperation.write_request:
                self.signal_write_complete[self.pending_idx_subidx].dispatch(self.pending_write_data)
                self.pending_operation = SdoOperation.none
                self.pending_idx_subidx = None
                self.pending_write_data = None

        elif isinstance(msg, CanOpenMessageSdoError):
            self.signal_error[self.pending_idx_subidx].dispatch(msg.error_msg,self.pending_operation)
            self.pending_operation = SdoOperation.none
