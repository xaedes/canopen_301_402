#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import can

from brave_new_world.constants import *
from brave_new_world.canopen_msgs.msg import CanOpenMessage
from brave_new_world.utils import collect_all_leaf_subclasses

from brave_new_world.canopen_msgs.msg_nmt_command import CanOpenMessageNmtCommand
from brave_new_world.canopen_msgs.msg_nmt_bootup import CanOpenMessageNmtBootup
from brave_new_world.canopen_msgs.msg_nmt_request import CanOpenMessageNmtRequest
from brave_new_world.canopen_msgs.msg_sdo_read_request import CanOpenMessageSdoReadRequest
from brave_new_world.canopen_msgs.msg_sdo_read_response import CanOpenMessageSdoReadResponse
from brave_new_world.canopen_msgs.msg_sdo_write_request import CanOpenMessageSdoWriteRequest
from brave_new_world.canopen_msgs.msg_sdo_write_response import CanOpenMessageSdoWriteResponse
from brave_new_world.canopen_msgs.msg_sdo_error import CanOpenMessageSdoError
        

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

