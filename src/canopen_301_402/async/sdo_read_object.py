#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from funcy import partial

from canopen_301_402.async.async_operation import AsyncOperation
from canopen_301_402.async.sdo_read import SdoRead


class SdoReadObject(AsyncOperation):
    """docstring for SdoReadObject"""
    def __init__(self, node, parameter_name, *args, **kwargs):
        self.node = node
        if parameter_name not in self.node.eds.objects_by_name:
            print "SdoReadObject: parameter '%s' not found in eds file." % parameter_name
            raise ValueError()
        eds_obj = self.node.eds.objects_by_name[parameter_name]

        if eds_obj.subindex is None:
            raise ValueError()

        self.index = eds_obj.index
        self.subindex = eds_obj.subindex
        if self.node.object_dict[(self.index, self.subindex)] is None:
            self.node.init_object(self.index, self.subindex)

        self.read_operation = partial(SdoRead, node, self.index, self.subindex)

        if "timeout" not in kwargs:
            kwargs["timeout"] = node.atomic_timeout

        super(SdoReadObject, self).__init__(node, *args, **kwargs)
    
    def do(self):
        read = self.read_operation()
        read.start()
        read.evt_done.wait()
        if read.evt_success.isSet():
            # decode
            self.node.object_dict[(self.index, self.subindex)].update_raw_data(read.result)
            self.result = self.node.object_dict[(self.index, self.subindex)].value
            self.response_timestamp = read.response_timestamp
            self.on_success()
            return

        elif read.evt_timeout.isSet():
            self.on_timeout()
            return
        elif read.evt_fault.isSet():
            self.on_fault()
            return
