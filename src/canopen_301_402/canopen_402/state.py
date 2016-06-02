#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from flufl.enum import Enum
from canopen_301_402.constants import Can402StateCommand

class Can402State(Enum):
    # Kommunikation DE_7000_00030.PDF pg. 75
    
    start                  = 0
    not_ready_to_switch_on = 1 
    # first two states will be run through autonomously
    # the device will normally be in "switch_on_disabled"
    # after successful initialization
    switch_on_disabled     = 2
    ready_to_switch_on     = 3
    switched_on            = 4
    operation_enable       = 5
    quick_stop_active      = 6
    fault_reaction_active  = 7
    fault                  = 8

Can402StateTransitions = dict({
            Can402State.switch_on_disabled: [{
                    Can402StateCommand.shutdown:              Can402State.ready_to_switch_on
                }],
            Can402State.ready_to_switch_on: [{
                    Can402StateCommand.disable_voltage:       Can402State.switch_on_disabled,
                    Can402StateCommand.quick_stop:            Can402State.switch_on_disabled,
                    Can402StateCommand.switch_on:             Can402State.switched_on
                }],
            Can402State.switched_on: [{
                    Can402StateCommand.disable_voltage:       Can402State.switch_on_disabled,
                    Can402StateCommand.quick_stop:            Can402State.switch_on_disabled,
                    Can402StateCommand.shutdown:              Can402State.ready_to_switch_on,
                    Can402StateCommand.enable_operation:      Can402State.operation_enable
                }],
            Can402State.operation_enable: [{
                    Can402StateCommand.disable_voltage:       Can402State.switch_on_disabled,
                    Can402StateCommand.quick_stop:            Can402State.quick_stop_active,
                    Can402StateCommand.shutdown:              Can402State.ready_to_switch_on,
                    Can402StateCommand.disable_operation:     Can402State.switched_on
                }],
            Can402State.quick_stop_active: [{
                    Can402StateCommand.enable_operation:      Can402State.operation_enable,
                    Can402StateCommand.disable_voltage:       Can402State.switch_on_disabled
                }],
            Can402State.fault: [{
                    Can402StateCommand.fault_reset:           Can402State.switch_on_disabled
                }],
        })
