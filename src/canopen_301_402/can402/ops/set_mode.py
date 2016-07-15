#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from canopen_301_402.constants import *
from canopen_301_402.async.sdo_write_object import SdoWriteObject

class SetMode(SdoWriteObject):
    """docstring for SetMode"""
    def __init__(self, node, mode, *args, **kwargs):
    	# print mode.value
    	parameter_name = "Modes of Operation"
        value = mode.value
        # index, subindex = Can402Objects.modes_of_operation_set

        super(SetMode, self).__init__(node, parameter_name, value, *args, **kwargs)
        
