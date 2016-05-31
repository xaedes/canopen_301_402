#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import struct

from canopen_301_402.utils import collect_all_leaf_subclasses

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
        @summary: returns decoded data
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

class CanDatatypeBoolean(CanDatatypeStruct):
    # '<' little endian
    # '?' bool
    data_format = "<?"

    @classmethod
    def identifier(cls):
        return 0x0001

    @classmethod
    def number_of_bits(cls):
        return 1


class CanDatatypeInt8(CanDatatypeStruct):
    # '<' little endian
    # 'b' signed char(int8)
    data_format = "<b"

    @classmethod
    def identifier(cls):
        return 0x0002

    @classmethod
    def number_of_bits(cls):
        return 8



class CanDatatypeInt16(CanDatatypeStruct):
    # '<' little endian
    # 'h' signed short (int16)
    data_format = "<h"

    @classmethod
    def identifier(cls):
        return 0x0003

    @classmethod
    def number_of_bits(cls):
        return 16

class CanDatatypeInt32(CanDatatypeStruct):
    # '<' little endian
    # 'i' signed int (int32)
    data_format = "<i"

    @classmethod
    def identifier(cls):
        return 0x0004

    @classmethod
    def number_of_bits(cls):
        return 32

class CanDatatypeUInt8(CanDatatypeStruct):
    # '<' little endian
    # 'b' unsigned char(uint8)
    data_format = "<B"

    @classmethod
    def identifier(cls):
        return 0x0005

    @classmethod
    def number_of_bits(cls):
        return 8

class CanDatatypeUInt16(CanDatatypeStruct):
    # '<' little endian
    # 'H' unsigned short (uint16)
    data_format = "<H"

    @classmethod
    def identifier(cls):
        return 0x0006

    @classmethod
    def number_of_bits(cls):
        return 16

class CanDatatypeUInt32(CanDatatypeStruct):
    # '<' little endian
    # 'I' unsigned int (uint32)
    data_format = "<I"

    @classmethod
    def identifier(cls):
        return 0x0007

    @classmethod
    def number_of_bits(cls):
        return 32

class CanDatatypeFloat32(CanDatatypeStruct):
    # '<' little endian
    # 'f' single precision floating point (float)
    data_format = "<f"

    @classmethod
    def identifier(cls):
        return 0x0008

    @classmethod
    def number_of_bits(cls):
        return 32

class CanDatatypes(object):
    def __init__(self):
        self.all_datatypes = collect_all_leaf_subclasses(CanDatatype)
        self.datatypes = dict()
        for datatype in self.all_datatypes:
            self.datatypes[datatype.identifier()] = datatype
            