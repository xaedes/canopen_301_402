#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from canopen_301_402.constants import *
from canopen_301_402.async.sdo_write import SdoWrite

class Set402Mode(SdoWrite):
    """docstring for Set402Mode"""
    def __init__(self, node, mode, *args, **kwargs):

        data = [Can402ModesOfOperationBits[mode]]
        index, subindex = Can402Objects.modes_of_operation_set

        super(Set402Mode, self).__init__(node, index, subindex, data, *args, **kwargs)
        
