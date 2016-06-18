#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import can

from canopen_301_402.constants import *
from canopen_301_402.canopen_msgs.msg import CanOpenMessage
from canopen_301_402.utils import collect_all_leaf_subclasses

from canopen_301_402.canopen_msgs.msg_nmt_command import CanOpenMessageNmtCommand
from canopen_301_402.canopen_msgs.msg_nmt_bootup import CanOpenMessageNmtBootup
from canopen_301_402.canopen_msgs.msg_nmt_request import CanOpenMessageNmtRequest
from canopen_301_402.canopen_msgs.msg_sdo_read_request import CanOpenMessageSdoReadRequest
from canopen_301_402.canopen_msgs.msg_sdo_read_response import CanOpenMessageSdoReadResponse
from canopen_301_402.canopen_msgs.msg_sdo_write_request import CanOpenMessageSdoWriteRequest
from canopen_301_402.canopen_msgs.msg_sdo_write_response import CanOpenMessageSdoWriteResponse
from canopen_301_402.canopen_msgs.msg_sdo_error import CanOpenMessageSdoError
        

class CanOpenMessages(object):
    """Message factory"""
    def __init__(self, canopen):
        super(CanOpenMessages, self).__init__()
        self.canopen = canopen

        self.all_message_types = collect_all_leaf_subclasses(CanOpenMessage)

    def try_to_upgrage_canopen_message(self, msg):
        '''
        @summary: Tries to upgrade CanOpenMessage into one of its subclasses, returns original CanOpenMessage on fail
        @param msg: CanOpenMessage
        @result: msg of either type CanOpenMessage or subclass of CanOpenMessage
        '''
        for msg_type in self.all_message_types:
            upgraded = msg_type.try_from_canopen_msg(msg, self.canopen)
            if upgraded is not None:
                return upgraded
        return msg

