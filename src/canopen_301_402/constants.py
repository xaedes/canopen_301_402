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

class Can402StateCommand(Enum):
    shutdown          = 0 # 2,6,8
    switch_on         = 1 # 3
    disable_voltage   = 2 # 7,9,10,12
    quick_stop        = 3 # 7,10,11
    disable_operation = 4 # 5
    enable_operation  = 5 # 4,16
    fault_reset       = 6 # 15

'''
@summary: Bits to be set in controlword; masked with Can402StateCommandMask
'''
Can402StateCommandBits = dict({
    Can402StateCommand.shutdown          = 0b0110,
    Can402StateCommand.switch_on         = 0b0111,
    Can402StateCommand.disable_voltage   = 0b0000,
    Can402StateCommand.quick_stop        = 0b0010,
    Can402StateCommand.disable_operation = 0b0111, 
    Can402StateCommand.enable_operation  = 0b1111,
    # normally we only change the 4 lowest bits, but for fault reset
    # we need to set the 8th bit
    Can402StateCommand.fault_reset       = 0b10000000 
    })

Can402StateCommandMask = dict({
    Can402StateCommand.shutdown          = 0b0111 
    Can402StateCommand.switch_on         = 0b1111
    Can402StateCommand.disable_voltage   = 0b0010
    Can402StateCommand.quick_stop        = 0b0110
    Can402StateCommand.disable_operation = 0b1111
    Can402StateCommand.enable_operation  = 0b1111
    # normally we only change the 4 lowest bits, but for fault reset
    # we need to set the 8th bit
    Can402StateCommand.fault_reset       = 0b10000000
    })

class Can402Objects(object):
    controlword = (0x6040,0x00)
    statusword  = (0x6041,0x00)

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

