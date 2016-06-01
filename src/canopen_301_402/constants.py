#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from flufl.enum import Enum

class CanFunctionCode(object): # todo better name, Kommunikation_DE_7000_00030.PDF pg. 69
    nmt  = 0b0000 # node_id must be 0
    sync = 0b0001 # node_id must be 0
    emergency = 0b0001
    pdo1_tx = 0b0011
    pdo1_rx = 0b0100
    pdo2_tx = 0b0101
    pdo2_rx = 0b0110
    pdo3_tx = 0b0111
    pdo3_rx = 0b1000
    sdo_tx = 0b1011
    sdo_rx = 0b1100
    nmt_error_control = 0b1110   

class CanData(Enum): # todo better name
    sdo_upload_request = 0x40        # 0b 0100 0000
    sdo_upload_response = 0x43       # 0b 0100 0011
    sdo_download_request_bits = 0x23 # 0b 0010 0011 
    sdo_download_response = 0x60     # 0b 0110 0000 
    sdo_error = 0x80


class Can301StateCommand(Enum):
    start_remote_node = 0x01
    enter_pre_operational = 0x80
    stop_remote_node = 0x02
    reset_node = 0x81
    reset_communication = 0x82

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

