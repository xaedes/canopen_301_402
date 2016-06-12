#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from flufl.enum import Enum

# class CanFunctionCode(object): # todo better name, Kommunikation_DE_7000_00030.PDF pg. 69
#     nmt  = 0b0000 # node_id must be 0
#     sync = 0b0001 # node_id must be 0
#     emergency = 0b0001
#     pdo1_tx = 0b0011
#     pdo1_rx = 0b0100
#     pdo2_tx = 0b0101
#     pdo2_rx = 0b0110
#     pdo3_tx = 0b0111
#     pdo3_rx = 0b1000
#     pdo4_tx = 0b1001
#     pdo4_rx = 0b1010
#     sdo_tx = 0b1011
#     sdo_rx = 0b1100
#     nmt_error_control = 0b1110


class CanOpenBasicDatatypes(Enum):
    boolean = 0x0001
    int8 = 0x0002
    int16 = 0x0003
    int32 = 0x0004
    uint8 = 0x0005
    uint16 = 0x0006
    uint32 = 0x0007
    float32 = 0x0008

class CanOpenMessageType(Enum):
    not_specified = 0
    nmt_command = 1
    nmt_request = 2
    sdo_write_request = 3
    sdo_write_response = 4
    sdo_read_request = 5
    sdo_read_response = 6
        

class CanOpenService(Enum):
    nmt               = 0
    sync              = 1
    emergency         = 2
    pdo1_tx           = 3
    pdo1_rx           = 4
    pdo2_tx           = 5
    pdo2_rx           = 6
    pdo3_tx           = 7
    pdo3_rx           = 8
    pdo4_tx           = 9
    pdo4_rx           = 10
    sdo_tx            = 11
    sdo_rx            = 12
    nmt_error_control = 13

CanOpenBroadcastServices = [CanOpenService.nmt, CanOpenService.sync]

CanOpenPredefinedConnectionSet = dict({
    CanOpenService.nmt:               0b0000,
    CanOpenService.sync:              0b0001,
    CanOpenService.emergency:         0b0001,
    CanOpenService.pdo1_tx:           0b0011,
    CanOpenService.pdo1_rx:           0b0100,
    CanOpenService.pdo2_tx:           0b0101,
    CanOpenService.pdo2_rx:           0b0110,
    CanOpenService.pdo3_tx:           0b0111,
    CanOpenService.pdo3_rx:           0b1000,
    CanOpenService.pdo4_tx:           0b1001,
    CanOpenService.pdo4_rx:           0b1010,
    CanOpenService.sdo_tx:            0b1011,
    CanOpenService.sdo_rx:            0b1100,
    CanOpenService.nmt_error_control: 0b1110
    })

class CanData(object): # todo better name
    sdo_upload_request        = 0x40 # 0b 0100 0000
    sdo_upload_response       = 0x43 # 0b 0100 0011
    sdo_download_request_bits = 0x23 # 0b 0010 0011 
    sdo_download_response     = 0x60 # 0b 0110 0000 
    sdo_error                 = 0x80


class Can301StateCommand(Enum):
    start_remote_node     = 0
    enter_pre_operational = 1
    stop_remote_node      = 2
    reset_node            = 3
    reset_communication   = 4

Can301StateCommandBits = dict({
    Can301StateCommand.start_remote_node:     0x01,
    Can301StateCommand.enter_pre_operational: 0x80,
    Can301StateCommand.stop_remote_node:      0x02,
    Can301StateCommand.reset_node:            0x81,
    Can301StateCommand.reset_communication:   0x82,
    })

class Can301State(Enum):
    initialisation  = 0
    pre_operational = 1
    operational     = 2
    stopped         = 3 # no sdo and bdo access, only nmt to change state

Can301StateTransitions = dict({
            Can301State.pre_operational: {
                    Can301StateCommand.reset_communication: Can301State.initialisation,
                    Can301StateCommand.reset_node:          Can301State.initialisation,
                    Can301StateCommand.start_remote_node:   Can301State.operational,
                    Can301StateCommand.stop_remote_node:    Can301State.stopped
                },
            Can301State.operational: {
                    Can301StateCommand.reset_communication:   Can301State.initialisation,
                    Can301StateCommand.reset_node:            Can301State.initialisation,
                    Can301StateCommand.enter_pre_operational: Can301State.pre_operational,
                    Can301StateCommand.stop_remote_node:      Can301State.stopped
                },
            Can301State.stopped: {
                    Can301StateCommand.reset_communication:   Can301State.initialisation,
                    Can301StateCommand.reset_node:            Can301State.initialisation,
                    Can301StateCommand.enter_pre_operational: Can301State.pre_operational,
                    Can301StateCommand.start_remote_node:     Can301State.operational
                },
        })

class Can402StateCommand(Enum):
    shutdown          = 0 # 2,6,8
    switch_on         = 1 # 3
    disable_voltage   = 2 # 7,9,10,12
    quick_stop        = 3 # 7,10,11
    disable_operation = 4 # 5
    enable_operation  = 5 # 4,16
    fault_reset       = 6 # 15

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
            Can402State.switch_on_disabled: {
                    Can402StateCommand.shutdown:              Can402State.ready_to_switch_on
                },
            Can402State.ready_to_switch_on: {
                    Can402StateCommand.disable_voltage:       Can402State.switch_on_disabled,
                    Can402StateCommand.quick_stop:            Can402State.switch_on_disabled,
                    Can402StateCommand.switch_on:             Can402State.switched_on
                },
            Can402State.switched_on: {
                    Can402StateCommand.disable_voltage:       Can402State.switch_on_disabled,
                    Can402StateCommand.quick_stop:            Can402State.switch_on_disabled,
                    Can402StateCommand.shutdown:              Can402State.ready_to_switch_on,
                    Can402StateCommand.enable_operation:      Can402State.operation_enable
                },
            Can402State.operation_enable: {
                    Can402StateCommand.disable_voltage:       Can402State.switch_on_disabled,
                    Can402StateCommand.quick_stop:            Can402State.quick_stop_active,
                    Can402StateCommand.shutdown:              Can402State.ready_to_switch_on,
                    Can402StateCommand.disable_operation:     Can402State.switched_on
                },
            Can402State.quick_stop_active: {
                    Can402StateCommand.enable_operation:      Can402State.operation_enable,
                    Can402StateCommand.disable_voltage:       Can402State.switch_on_disabled
                },
            Can402State.fault: {
                    Can402StateCommand.fault_reset:           Can402State.switch_on_disabled
                },
        })


'''
@summary: Bits to be set in controlword; masked with Can402StateCommandMask
'''
Can402StateCommandBits = dict({
    Can402StateCommand.shutdown          : 0b0110,
    Can402StateCommand.switch_on         : 0b0111,
    Can402StateCommand.disable_voltage   : 0b0000,
    Can402StateCommand.quick_stop        : 0b0010,
    Can402StateCommand.disable_operation : 0b0111, 
    Can402StateCommand.enable_operation  : 0b1111,
    # normally we only change the 4 lowest bits, but for fault reset
    # we need to set the 8th bit
    Can402StateCommand.fault_reset       : 0b10000000 
    })

Can402StateCommandMask = dict({
    Can402StateCommand.shutdown          : 0b0111, 
    Can402StateCommand.switch_on         : 0b1111,
    Can402StateCommand.disable_voltage   : 0b0010,
    Can402StateCommand.quick_stop        : 0b0110,
    Can402StateCommand.disable_operation : 0b1111,
    Can402StateCommand.enable_operation  : 0b1111,
    # normally we only change the 4 lowest bits, but for fault reset
    # we need to set the 8th bit
    Can402StateCommand.fault_reset       : 0b10000000
    })

class Can402Objects(object):
    controlword = (0x6040,0x00)
    statusword  = (0x6041,0x00)
    modes_of_operation_set = (0x6060,0x00)
    modes_of_operation_get = (0x6061,0x00)
    target_position = (0x607A,0x00)

Can402StatuswordStateBits = dict({
    Can402State.not_ready_to_switch_on  : 0b0000000,
    Can402State.switch_on_disabled      : 0b1000000,
    Can402State.ready_to_switch_on      : 0b0100001,
    Can402State.switched_on             : 0b0100011,
    Can402State.operation_enable        : 0b0100111,
    Can402State.quick_stop_active       : 0b0000111,
    Can402State.fault_reaction_active   : 0b0001111,
    Can402State.fault                   : 0b0001000
    })

Can402StatuswordStateMasks = dict({
    Can402State.not_ready_to_switch_on  : 0b1001111,
    Can402State.switch_on_disabled      : 0b1001111,
    Can402State.ready_to_switch_on      : 0b1101111,
    Can402State.switched_on             : 0b1101111,
    Can402State.operation_enable        : 0b1101111,
    Can402State.quick_stop_active       : 0b1101111,
    Can402State.fault_reaction_active   : 0b1001111,
    Can402State.fault                   : 0b1001111
    })

class Can402ControlwordBits(object):
    switch_on = 0
    enable_voltage = 1
    quick_stop = 2
    enable_operation = 3
    new_set_point = 4
    change_set_immediately = 5
    abs_rel = 6
    fault_reset = 7
    halt = 8

class Can402StatuswordBits(object):
    ready_to_switch_on = 0
    switched_on = 1
    operation_enabled = 2
    fault = 3
    voltage_enable = 4
    quick_stop = 5
    switch_on_disabled = 6
    warning = 7 # not in use
    unused_0 = 8 
    remote = 9 # not in use
    target_reached = 10
    internal_limit_active = 11
    set_point_ack = 12
    homing_error = 13
    hard_notify = 14
    unused_1 = 15

class Can402ModesOfOperation(Enum):
    position = 0
    velocity = 1
    homing = 2
    
Can402ModesOfOperationBits = {
    Can402ModesOfOperation.position: 1,
    Can402ModesOfOperation.velocity: 3,
    Can402ModesOfOperation.homing: 6
}
        

# Kommunikation DE_7000_00030.PDF pg. 64
# https://github.com/rscada/libcanopen/blob/master/canopen/canopen.c
CanErrors = dict({
        0x05030000: "toggle bit not changed",
        0x05040000: "sdo protocol timed out",
        0x05040001: "sdo command specifier not valid",
        0x05040002: "invalid block size (block transfer mode only)",
        0x05040003: "invalid sequence number (block transfer mode only)",
        0x05040004: "crc error (block transfer mode only)",
        0x05040005: "out of memory",
        0x06010000: "access to this object not supported",
        0x06010001: "try to read a write-only object",
        0x06010002: "try to write to read-only object",
        0x06020000: "object not existing in object dictionary",
        0x06040041: "object can not be mapped in PDO",
        0x06040042: "number and/or length of mapped objects would exceed PDO length",
        0x06040043: "general parameter incompatibility",
        0x06040047: "general internal device error",
        0x06060000: "access aborted due to hardware error",
        0x06070010: "data type or parameter length does not match or not known",
        0x06070012: "data type does not match: parameter length to high",
        0x06070013: "data type does not match: parameter length to low",
        0x06090011: "subindex not existing",
        0x06090030: "general domain error",
        0x06090031: "domain error: parameter value to big",
        0x06090032: "domain error: parameter value to small",
        0x06090036: "maximum value is less then minimum value",
        0x060A0023: "resource not available",
        0x08000000: "general error",
        0x08000020: "access not available",
        0x08000021: "access not available due to local application",
        0x08000022: "access not available due to current device state",
        0x08000023: "object dictionary dynamic generation fails or no object dictionary is present (e.g. OD is generated from file and generation fails because of a file error)",
        "unknown":  "Unknown error code: %s"
    })

class CanOpenObjectAttribute(Enum):
    #301_v04020005_cor3.pdf pg. 90 
    rw    = 0 # read and write access
    wo    = 1 # write only access
    ro    = 2 # read only access
    const = 3 # read only access, value is constant 
              # The value may change in NMT state Initialisation. 
              # The value shall not change in the NMT states pre-
              # operation, operational and stopped. 
                    

class CanOpenObjectType(Enum):
    #301_v04020005_cor3.pdf pg. 89 
    null      = 0x00  # object with no data fields
    domain    = 0x02  # large variable amount of data e.g. executable program code 
    deftype   = 0x05  # denotes a type definition such as a BOOLEAN, UNSIGNED16, FLOAT and so on 
    defstruct = 0x06  # defines a new record type e.g. the PDO mapping structure at 21 h  
    var       = 0x07  # A single value such as an UNSIGNED8, BOOLEAN, FLOAT, INTEGER16, VISIBLE STRING etc. 
    array     = 0x08  # A multiple data field object where each data field is a simple variable of the
                      # SAME basic data type e.g. array of UNSIGNED16 etc. Sub-index 0 is of UNSIGNED8 
                      # and therefore not part of the ARRAY data         
    record    = 0x09  # A multiple data field object where the 
                      # data fields may be any combination of 
                      # simple variables. Sub-index 0 is of 
                      # UNSIGNED8 and sub-index 255 is of 
                      # UNSIGNED32 and therefore not part 
                      # of the RECORD data 

