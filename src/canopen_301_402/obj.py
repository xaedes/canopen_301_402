#!/usr/bin/env python2
# -*- coding: utf-8 -*-

class CanOpenObject(object):
    def __init__(self, node, index, subindex):
        super(CanOpenObject, self).__init__()
        self.node = node
        self.canopen = self.node.canopen
        self.index = index
        self.subindex = subindex

        self.datatype_id = 0x0
        self._value = None
        self._raw_data = None
        # get eds object definition
        self.eds_obj = self.node.eds.get_object(index, subindex)

        # print "CanOpenObject"
        # print hex(index), hex(subindex), 
        # print self.eds_obj

        if self.eds_obj is not None:
            # if there is an eds object definition assign datatype and defaults
            self.datatype_id = self.eds_obj.datatype
            self._value = self.eds_obj.default_value

        
    def update_raw_data(self,raw_data):
        self._raw_data = raw_data
        if self.datatype is not None:
            self._value = self.datatype.decode(bytearray(self._raw_data))
        else:
            self._value = self._raw_data

    @property
    def value(self):
        return self._value

    @property
    def raw_data(self):
        return self._raw_data
        
    @property
    def datatype(self):
        '''
        @summary: CanDatatype 
        @result: 
        '''
        if self.datatype_id in self.node.datatypes.datatypes:
            return self.node.datatypes.datatypes[self.datatype_id]
        else:
            return None
    