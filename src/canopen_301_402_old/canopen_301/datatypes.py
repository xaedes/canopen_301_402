#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import struct

from canopen_301_402.utils import collect_all_leaf_subclasses
from canopen_301_402.utils import parseIntAutoBase

from canopen_301_402.constants import CanOpenBasicDatatypes

class CanDatatype(object):
    def __init__(self):
        '''
        @summary: abstract base class for all can datatypes
        @raises:  NotImplemented
        '''
        raise NotImplemented

    def identifier(self):
        '''
        @summary: return standard data type identifier
        @param self:
        @result: uint16 containing data type identifier

        @see http://atlas.web.cern.ch/Atlas/GROUPS/DAQTRIG/DCS/LMB/PROFILE/cano-eds.htm
        '''
        raise NotImplemented

    def number_of_bits(self):
        '''
        @summary: returns number of bits for one value encoded with this datatype
        @param self:
        @result: number of bits
        '''
        raise NotImplemented

    def decode(self, data):
        '''
        @summary: returns value of decoded data
        @param self:
        @param data: byte array
        @result: value
        '''
        raise NotImplemented

    def encode(self, value):
        '''
        @summary: returns encoded value
        @param self:
        @param value: value to be encoded
        @result: data byte array
        '''
        raise NotImplemented

    def decode_string(self, string):
        '''
        @summary: returns value of human readable representation
        @param self:
        @param string: human readable representation of value as string
        @result: value
        '''
        raise NotImplemented

    def encode_string(self, value):
        '''
        @summary: returns human readable representation
        @param self:
        @param value: value to be encoded
        @result: human readable representation of value as string
        '''
        raise NotImplemented

class CanDatatypeStruct(CanDatatype):
    def __init__(self, identifier, struct_data_format):
        '''
        @summary: Can data type base class using python 'struct' module for data coding
        @param identifier:         specifies can datatype identifier 
        @param struct_data_format: specifies data format for struct.pack and struct.unpack
        
        example data_format "<i"
        '<' little endian
        'i' 32 bit signed integer

        '''
        self._identifier = identifier
        self._data_format = struct_data_format
        self._number_of_bits = struct.calcsize(self.data_format)*8
    
    def identifier(self):
        return self._identifier

    def number_of_bits(self):
        return self._number_of_bits

    @property
    def data_format(self):
        # '<' : little endian
        return '<' + self._data_format
    

    def decode(self, data):
        result = struct.unpack_from(self.data_format, data)

        # unpack value of length-1 tuples
        if len(result) == 1:
            value, = result
        
        return value

    def encode(self, value):
        return bytearray(struct.pack(self.data_format, value))

    def decode_string(self, string):
        # default implementation tries to interprete as integer number
        return parseIntAutoBase(string)

    def encode_string(self, value):
        return str(value)



class CanDatatypeFloat32(CanDatatypeStruct):
    def __init__(self):
        super(CanDatatypeFloat32,self).__init__(CanOpenBasicDatatypes.float32,"f")

    def decode_string(self, string):
        num_value = float(string)
        return num_value

class CanDatatypeBoolean(CanDatatypeStruct):
    def __init__(self):
        super(CanDatatypeBoolean,self).__init__(CanOpenBasicDatatypes.boolean,"?")

    def decode_string(self, string):
        # look for true/false keywords
        if str.lower(string).strip() == "true":
            return True
        elif str.lower(string).strip() == "false":
            return False

        # try to interprete as integer number
        num_value = parseIntAutoBase(string)
        
        if num_value is None: # interpretation failed
            return None
        else:
            return num_value != 0 # c interpretation of bool

class CanDatatypePDOMapping(CanDatatype):
    def __init__(self, node, identifier, num_mapped=0, mappings=list()):
        '''
        @summary: Can data type representing a pdo mapping
        @param identifier:                 specifies can datatype identifier 
        @param num_mapped:       number of currently mapped objects         
        @param mappings:         list of currently mapped object identifiers

        max_num_mappings will be constant after initialization
        num_mapped & max_num_mappings can still be updated (to remap the pdo)
        '''
        self.node = node
        self.canopen = node.canopen
        self._identifier = identifier
        self._num_mapped = num_mapped
        self.mappings = [0]*64 # max 64 mappings 301_v04020005_cor3.pdf pg. 93
        for k,mapping in enumerate(mappings):
            self.mappings[k] = mapping

    def identifier(self):
        return self._identifier

    def number_of_bits(self):
        return self._number_of_bits
    
    @property
    def num_mapped(self):
        return self._num_mapped

    @num_mapped.setter
    def num_mapped(self,v):
        if 0 <= v <= self.max_num_mappings:
            self._num_mapped = v
        else:
            raise ValueError()

    @property
    def data_format(self):
        result  = ""
        for obj_id in self.mappings[:self.num_mapped]:
            datatype = self.node.obj_dict.objects[obj_id].datatype
            if not hasattr(datatype,"_data_format"):
                raise RuntimeError()
            result += datatype._data_format
        return "<" + result
    

    def decode(self, data):
        obj_values = struct.unpack_from(self.data_format, data)
        return obj_values

    def encode(self, obj_values):
        return bytearray(struct.pack(self.data_format, obj_values))

    def decode_string(self, string):
        raise RuntimeError()

    def encode_string(self, value):
        raise RuntimeError()


class CanDatatypes(object):
    def __init__(self):
        # generate basic datatypes
        self.all_datatypes = list()
        self.all_datatypes.append(CanDatatypeStruct(CanOpenBasicDatatypes.int8,"b"))
        self.all_datatypes.append(CanDatatypeStruct(CanOpenBasicDatatypes.int16,"h"))
        self.all_datatypes.append(CanDatatypeStruct(CanOpenBasicDatatypes.int32,"i"))
        self.all_datatypes.append(CanDatatypeStruct(CanOpenBasicDatatypes.uint8,"B"))
        self.all_datatypes.append(CanDatatypeStruct(CanOpenBasicDatatypes.uint16,"H"))
        self.all_datatypes.append(CanDatatypeStruct(CanOpenBasicDatatypes.uint32,"I"))
        self.all_datatypes.append(CanDatatypeFloat32())
        self.all_datatypes.append(CanDatatypeBoolean())

        # add datatypes to dictionary mapping from its identifiers
        self.datatypes = dict()
        for datatype in self.all_datatypes:
            self.datatypes[datatype.identifier()] = datatype
            