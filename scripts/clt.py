#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division

import os
import readline
import struct
import re
import traceback

import can
from funcy import partial

from canopen_301_402.canopen import CanOpen
from canopen_301_402.canopen_msgs.msgs import *
from canopen_301_402.utils import *
from canopen_301_402.constants import *
from canopen_301_402.async.sdo_read import SdoRead

from canopen_301_402.node import CanOpenNode

RE_SPACE = re.compile('.*\s+$', re.M)
 
class CanRelated(object):
    def __init__(self):
        self.can_device = None
        self.node_id = None
        self.eds = None
        
        self.bus = None
        self.canopen = None
        self.node = None

        self.initialized = False

        self.timeout = 1.


class CommandLineTool(object):
    """docstring for CommandLineTool"""
    def __init__(self):
        super(CommandLineTool, self).__init__()
        self.running = False

        self.eds_files = [
            "/home/xaedes/gits/fahrrad/workspace/src/fahrrad_antrieb/src/fahrrad_antrieb/epos2.eds",
            "/home/xaedes/gits/fahrrad/eds/605.3150.68-B-EK-2-60.eds"
        ]

        self.can_devices = self.list_can_devices()
        self.commands = ["help","device","node","init","read","write","list","quit","eds"]

        self.can = CanRelated()
        self.can.can_device = self.can_devices[0]
        self.can.node_id = 1
        self.can.eds = self.eds_files[0]

        self.preset_can_objects = [field for field in dir(Can402Objects) if not field.startswith("_")]
        self._can_objects = dict()

        self.init_autocomplete()
        self.init_can()

        print self.can_objects

    @property
    def can_objects(self):
        return self._can_objects
        
    def update_can_objects(self):
        result = dict()
        for parameter_name in self.preset_can_objects:
            result[parameter_name] = getattr(Can402Objects,parameter_name)


        for parameter_name, obj in self.can.node.eds.objects_by_name.iteritems():
            if obj.subindex is not None:
                result[parameter_name.replace(" ","")] = obj.index, obj.subindex

        self._can_objects = result
    

    def _complete_arg(self, args, options, index=-1):
        if not args:
            return [option +" " for option in options]
        else:
            return [option +" " for option in options if option.startswith(args[-1])]


    def complete_commands(self):
        return [cmd + " " for cmd in self.commands]

    def complete_device(self, args):
        return self._complete_arg(args, self.can_devices)
        
    def complete_node(self, args):
        return self._complete_arg(args, map(str,[1,2]))

    def complete_read(self, args):
        return self._complete_arg(args, self.can_objects.iterkeys(), index=0)

    def complete_write(self, args):
        if len(args) > 0:
            return []
        else:
            return self._complete_arg(args, self.can_objects.iterkeys(), index=0)

    def complete_list(self, args):
        return []
        
    def complete_help(self, args):
        return []
        
    def complete_quit(self, args):
        return []

    def complete_eds(self, args):
        return self._complete_arg(args, self.eds_files)
        
    def commands_completer(self, text, state):
        # get already inputted text
        line_buffer = readline.get_line_buffer()

        # print "line_buffer '%s'" % line_buffer

        orig_len = len(line_buffer)
        line = line_buffer.lstrip()
        stripped = orig_len - len(line)
        begidx = readline.get_begidx() - stripped
        endidx = readline.get_endidx() - stripped        
        # print "orig_len", orig_len
        # print "line", line
        # print "stripped", stripped
        # print "begidx", begidx
        # print "endidx", endidx
        being_completed = line[begidx:endidx]

        # print "being_completed '%s'" % being_completed

        # print len(line), line

        line = line.split()
        # print "len(line)", len(line)

        if RE_SPACE.match(line_buffer):
            line.append('')

        # print type(line)
        # print line
        # print "len(line)", len(line)

        if not line:
            # shows all commands
            return self.complete_commands()[state]

        # determine command
        cmd = line[0].strip()

        if cmd in self.commands:
            # resolve command
            impl = getattr(self, "complete_" + cmd)
            args = line[1:]
            completions = impl(args) + [None]
            # results = [c for c in completions if c.startswith(cmd)] + [None]
            return completions[state]

            # [state]

        else:
            # complete command
            # return [cmd + ' '][state]
            results = [c for c in self.complete_commands() if c.startswith(cmd)] + [None]
            return results[state]

    def init_autocomplete(self):
        readline.set_completer(self.commands_completer)
        readline.parse_and_bind("tab: complete")

    def stop_can_node(self):
        if self.can.node is not None and self.can.node.thread is not None:
            self.can.node.running = False
            self.can.node.thread.join()

    def init_can(self):
        self.initialized = False
        try:
            self.can.bus = can.interface.Bus(self.can.can_device, bustype='socketcan_ctypes')
            self.can.canopen = CanOpen(self.can.bus)

            self.stop_can_node()

            self.can.node = CanOpenNode(self.can.canopen,node_id=self.can.node_id)
            self.can.node.eds.read(self.can.eds)

            self.update_can_objects()
            for index, subindex in self.can_objects.itervalues():
                self.can.node.init_object(index, subindex)

            self.can.node.start_thread()
            self.initialized = True
            print "CanOpen successful initialized:"
            print "\tcan device: %s" % self.can.can_device
            print "\tnode id: %d" % self.can.node_id
            print "\teds: %s" % self.can.eds

        except Exception, e:
            traceback.print_exc()
            raise e

    def list_can_devices(self):
        return ["can0","vcan0"]

    def parse(self, inp):
        words = [word.strip() for word in inp.lstrip().split()]

        if not words:
            cmd = None
        else:
            cmd = words[0]
            args = words[1:]

        if cmd not in self.commands:
            return None, inp
        else:
            return cmd, args


    def can_object_valid(self, obj):
        return hasattr(Can402Objects, obj)
        # return obj in self.can_objects

    def parse_can_object(self, obj_name):
        if obj_name not in self.can_objects:
            return None
        else:
            return self.can_objects[obj_name]


    def is_parseable_number(self, str):
        try:
            parseIntAutoBase(str)
            return True
        except ValueError:
            return False


    def cmd_device(self, args):
        if not args or args[0] not in self.can_devices:
            raise ValueError()

        # set can device
        self.can.can_device = args[0]
        print "Ok, set can device to '%s'." % self.can.can_device
        self.init_can()


    def cmd_node(self, args):
        if not args or not self.is_parseable_number(args[0]):
            raise ValueError()

        self.can.node_id = parseIntAutoBase(args[0])
        print "Ok, set node id to '%d' (decimal)." % self.can.node_id
        self.init_can()



    def cmd_read(self, args):
        if not args or not self.parse_can_object(args[0]):
            raise ValueError()
        index, subindex = self.parse_can_object(args[0])
        read = SdoRead(self.can.node, index, subindex, timeout=self.can.timeout)
        read.start()
        read.evt_done.wait()
        if read.evt_success.isSet():
            print "raw data:"
            for byte in read.result:
                print hex(byte),

            self.can.node.object_dict[(index, subindex)].update_raw_data(read.result)

            print ""
            print "decoded value:", self.can.node.object_dict[(index, subindex)].value

            # print bytearray(read.result)
        elif read.evt_timeout.isSet():
            print "timeout"
        elif read.evt_fault.isSet():
            print "fault"

    def cmd_write(self, args):
        if len(args)<2 or not self.parse_can_object(args[0]):
            raise ValueError()
        index, subindex = self.parse_can_object(args[0])
        write = SdoWrite(self.can.node, index, subindex, data, timeout=self.can.timeout)
        write.start()
        write.evt_done.wait()

        if write.evt_success.isSet():
            print "Write success"

        elif read.evt_timeout.isSet():
            print "timeout"
        elif read.evt_fault.isSet():
            print "fault"

    def cmd_eds(self, args):
        if not args:
            print "  Missing parameter!"
            print "  Please specify path to eds file like this:"
            print "  > eds /path/to/file.eds"
            return

        original_value = self.can.eds
        self.can.eds = args[0]

        print "Ok, set eds file to '%s'." % self.can.eds

        try:
            self.init_can()
        except:
            print "Error during CAN init. Set eds file to old value '%s'." % original_value
            self.can.eds = original_value

            self.init_can()



    def cmd_init(self, args):
        self.init_can()

    def cmd_quit(self, args):
        self.running = False
        self.stop_can_node()


    def cmd_list(self, args):
        pass

    def cmd_help(self, args):
        print "available commands: " + ",".join(self.commands)

    def spin(self):
        self.running = True
        while self.running:
            # print self.can.__dict__
            inp = raw_input("> ")
            # print "You entered '%s'" % inp
            
            cmd, args = self.parse(inp)
            # print "cmd, args:", cmd, args

            if cmd is not None:
                impl = getattr(self, "cmd_" + cmd)
                impl(args)
                # try:
                    # impl(args)
                # except ValueError, e:
# 
                    # raise e

                # print "Execute cmd %s" % cmd
            # print inp == self.commands_completer(inp,0)
        
def main():
    clt = CommandLineTool()
    clt.spin()
    
if __name__ == '__main__':
    main()