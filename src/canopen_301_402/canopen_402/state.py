#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from flufl.enum import Enum
from canopen_301_402.constants import Can402StateCommand

class Can402State(Enum):
    pass
    # todo 

    
    # initialisation = 0
    # pre_operational = 1
    # operational = 2
    # stopped = 3 # no sdo and bdo access, only nmt to change state

    # Transitions = None

# Can402State.Transitions = dict({
#             Can402State.pre_operational: [{
#                     Can402StateCommand.reset_communication: Can402State.initialisation,
#                     Can402StateCommand.reset_node:          Can402State.initialisation,
#                     Can402StateCommand.start_remote_node:   Can402State.operational,
#                     Can402StateCommand.stop_remote_node:    Can402State.stopped
#                 }],
#             Can402State.operational: [{
#                     Can402StateCommand.reset_communication:   Can402State.initialisation,
#                     Can402StateCommand.reset_node:            Can402State.initialisation,
#                     Can402StateCommand.enter_pre_operational: Can402State.pre_operational,
#                     Can402StateCommand.stop_remote_node:      Can402State.stopped
#                 }],
#             Can402State.stopped: [{
#                     Can402StateCommand.reset_communication:   Can402State.initialisation,
#                     Can402StateCommand.reset_node:            Can402State.initialisation,
#                     Can402StateCommand.enter_pre_operational: Can402State.pre_operational,
#                     Can402StateCommand.start_remote_node:     Can402State.operational
#                 }],
#         })
