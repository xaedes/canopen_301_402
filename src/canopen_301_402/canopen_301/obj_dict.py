#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from collections import defaultdict

from canopen_301_402.constants import *

class CanOpenObjectDictionary(object):
    """docstring for CanOpenObjectDictionary"""
    def __init__(self, canopen):
        super(CanOpenObjectDictionary, self).__init__()
        self.canopen
        self.objects = defaultdict(lambda:None)
        self.datatypes = defaultdict(lambda:None)
        self.populate_with_defaults()
        self.populate_from_eds()
        
    def populate_with_defaults(self):
        # set both to uint16
        self.datatypes[Can402Objects.controlword] = self.canopen.datatypes.datatypes[CanOpenBasicDatatypes.uint16]
        self.datatypes[Can402Objects.statusword] = self.canopen.datatypes.datatypes[CanOpenBasicDatatypes.uint16]
        self.objects[Can402Objects.controlword] = 0x0000
        self.objects[Can402Objects.statusword] = 0x0000

    def populate_from_eds(self, eds=None):
        if eds is None:
            eds = self.canopen.eds

        def check_uint16(index,subindex):
            if index in eds.optional_objects.objects:
                datatype_num = eds.optional_objects.objects[index].datatype
                if datatype_num != CanOpenBasicDatatypes.uint16:
                    # eds file specifies other datatype then uint16
                    raise NotImplemented()

        # only check for correct type of controlword and statusword for now
        check_uint16(*Can402Objects.controlword)
        check_uint16(*Can402Objects.statusword)

        def load_value_from_eds(index,subindex):
            if subindex > 0: raise NotImplemented()
            
            if index in eds.optional_objects.objects:
                datatype = self.datatypes[(index,subindex)]

                default_value = datatype.decode_string(eds.optional_objects.objects[index].default_value)
                if default_value is not None:
                    self.objects[(index,subindex)] = default_value

        load_value_from_eds(*Can402Objects.controlword)
        load_value_from_eds(*Can402Objects.statusword)
