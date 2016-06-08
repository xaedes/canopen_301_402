#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from collections import defaultdict

import can

from canopen_301_402.constants import *
from canopen_301_402.assertions import Assertions
from canopen_301_402.canopen_301.state import Can301State,Can301StateTransitions
from canopen_301_402.canopen_msgs.msg import CanOpenMessage
from canopen_301_402.canopen_msgs.msgs import *
from canopen_301_402.canopen_301.service import CanOpenServiceBaseClass


class CanOpenNetworkManagement(CanOpenServiceBaseClass):
    '''
    @summary: for use as cooperative base class in CanOpen
    '''
    def __init__(self, *args, **kwargs):
        super(CanOpenNetworkManagement, self).__init__(*args, **kwargs)

    def process_msg(self, msg):
        if isinstance(msg, CanOpenMessageNmtBootup):
            # device starts in state initialization
            # boot up message signals end of initialization
            if self.node.state == Can301State.initialisation:
                self.node.state = Can301State.pre_operational
                print "changed 301 state to",self.node.state
                
        elif isinstance(msg, CanOpenMessageNmtCommand):
            # change state according to nmt command
            if self.node.state in Can301StateTransitions:
                transitions = Can301StateTransitions[self.node.state]
                self.node.state = transitions[command]
            

                print "changed 301 state to",self.node.state
