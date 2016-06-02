#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import struct

from canopen_301_402.utils import collect_all_leaf_subclasses
from canopen_301_402.utils import parseIntAutoBase

from canopen_301_402.constants import CanOpenBasicDatatypes

class CanDatatype(object):
    '''
    @summary: abstract base class for all can datatypes
    '''

    @classmethod
    def identifier(cls):
        '''
        @summary: return standard data type identifier
        @param cls:
        @result: uint16 containing data type identifier

        @see http://atlas.web.cern.ch/Atlas/GROUPS/DAQTRIG/DCS/LMB/PROFILE/cano-eds.htm
        '''
        raise NotImplemented

    @classmethod
    def number_of_bits(cls):
        '''
        @summary: returns number of bits for one value encoded with this datatype
        @param cls:
        @result: number of bits
        '''
        raise NotImplemented

    @classmethod
    def decode(cls, data):
        '''
        @summary: returns value of decoded data
        @param cls:
        @param data: byte array
        @result: value
        '''
        raise NotImplemented

    @classmethod
    def encode(cls, value):
        '''
        @summary: returns encoded value
        @param cls:
        @param value: value to be encoded
        @result: data byte array
        '''
        raise NotImplemented

    @classmethod
    def decode_string(cls, string):
        '''
        @summary: returns value of human readable representation
        @param cls:
        @param string: human readable representation of value as string
        @result: value
        '''
        raise NotImplemented

    @classmethod
    def encode_string(cls, value):
        '''
        @summary: returns human readable representation
        @param cls:
        @param value: value to be encoded
        @result: human readable representation of value as string
        '''
        raise NotImplemented

class CanDatatypeStruct(CanDatatype):
    '''
    @summary: can data type base class using python 'struct' module for data coding
              you must specify data_format in a subclass
    '''
    
    # example data_format; overwrite this in a subclass
    # '<' little endian
    # 'i' 32 bit signed integer
    data_format = "<i"

    @classmethod
    def decode(cls, data):
        result = struct.unpack_from(cls.data_format, data)
        value, = result
        return value

    @classmethod
    def encode(cls, value):
        struct.pack(cls.data_format, value)

    @classmethod
    def decode_string(cls, string):
        # default implementation tries to interprete as integer number
        return parseIntAutoBase(string)

    @classmethod
    def encode_string(cls, value):
        return str(value)

class CanDatatypeBoolean(CanDatatypeStruct):
    # '<' little endian
    # '?' bool
    data_format = "<?"

    @classmethod
    def identifier(cls):
        return CanOpenBasicDatatypes.boolean

    @classmethod
    def number_of_bits(cls):
        return 1

    @classmethod
    def decode_string(cls, string):
        # default implementation tries to interprete as integer number
        num_value = parseIntAutoBase(string)
        
        if num_value is None:
            return None
        else:
            return num_value != 0 # c interpretation of bool

class CanDatatypeInt8(CanDatatypeStruct):
    # '<' little endian
    # 'b' signed char(int8)
    data_format = "<b"

    @classmethod
    def identifier(cls):
        return CanOpenBasicDatatypes.int8

    @classmethod
    def number_of_bits(cls):
        return 8



class CanDatatypeInt16(CanDatatypeStruct):
    # '<' little endian
    # 'h' signed short (int16)
    data_format = "<h"

    @classmethod
    def identifier(cls):
        return CanOpenBasicDatatypes.int16

    @classmethod
    def number_of_bits(cls):
        return 16

class CanDatatypeInt32(CanDatatypeStruct):
    # '<' little endian
    # 'i' signed int (int32)
    data_format = "<i"

    @classmethod
    def identifier(cls):
        return CanOpenBasicDatatypes.int32

    @classmethod
    def number_of_bits(cls):
        return 32

class CanDatatypeUInt8(CanDatatypeStruct):
    # '<' little endian
    # 'b' unsigned char(uint8)
    data_format = "<B"

    @classmethod
    def identifier(cls):
        return CanOpenBasicDatatypes.uint8

    @classmethod
    def number_of_bits(cls):
        return 8

class CanDatatypeUInt16(CanDatatypeStruct):
    # '<' little endian
    # 'H' unsigned short (uint16)
    data_format = "<H"

    @classmethod
    def identifier(cls):
        return CanOpenBasicDatatypes.uint16

    @classmethod
    def number_of_bits(cls):
        return 16

class CanDatatypeUInt32(CanDatatypeStruct):
    # '<' little endian
    # 'I' unsigned int (uint32)
    data_format = "<I"

    @classmethod
    def identifier(cls):
        return CanOpenBasicDatatypes.uin32

    @classmethod
    def number_of_bits(cls):
        return 32

class CanDatatypeFloat32(CanDatatypeStruct):
    # '<' little endian
    # 'f' single precision floating point (float)
    data_format = "<f"

    @classmethod
    def identifier(cls):
        return CanOpenBasicDatatypes.float32

    @classmethod
    def number_of_bits(cls):
        return 32

    @classmethod
    def decode_string(cls, string):
        num_value = float(string)
        return num_value

class CanDatatypes(object):
    def __init__(self):
        self.all_datatypes = collect_all_leaf_subclasses(CanDatatype)
        self.datatypes = dict()
        for datatype in self.all_datatypes:
            self.datatypes[datatype.identifier()] = datatype
            