#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from canopen_301_402.async.async_operation import AsyncOperation
from canopen_301_402.async.sdo_write import SdoWrite

from canopen_301_402.canopen_msgs.msgs import CanOpenMessageSdoWriteRequest
from canopen_301_402.canopen_msgs.msgs import CanOpenMessageSdoWriteResponse
from canopen_301_402.canopen_msgs.msgs import CanOpenMessageSdoError

class SdoWriteObject(SdoWrite):
    """docstring for SdoWrite"""
    def __init__(self, node, parameter_name, value, *args, **kwargs):
        self.node = node
        if parameter_name not in self.node.eds.objects_by_name:
            print "SdoWriteObject: parameter '%s' not found in eds file." % parameter_name
            raise ValueError()
        eds_obj = self.node.eds.objects_by_name[parameter_name]

        if eds_obj.subindex is None:
            raise ValueError()

        index = eds_obj.index
        subindex = eds_obj.subindex
        if self.node.object_dict[(index, subindex)] is None:
            self.node.init_object(index, subindex)

        datatype = self.node.object_dict[(index, subindex)].datatype
        if datatype is None:
            print "SdoWriteObject: no datatype for parameter '%s'" % (parameter_name)
            raise ValueError()
        data = datatype.encode(value)

        if "timeout" not in kwargs:
            kwargs["timeout"] = node.atomic_timeout

        super(SdoWriteObject, self).__init__(node, index, subindex, data, *args, **kwargs)
        