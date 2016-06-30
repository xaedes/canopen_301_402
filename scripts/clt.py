#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division

import os
import readline
import struct

import can
from funcy import partial

from canopen_301_402.canopen import CanOpen
from canopen_301_402.canopen_msgs.msgs import *
from canopen_301_402.utils import *
from canopen_301_402.constants import *
from canopen_301_402.async.sdo_read import SdoRead

from canopen_301_402.node import CanOpenNode


 
class CanRelated(object):
    def __init__(self):
        self.can_device = None
        self.node_id = None
        self.eds = None
        
        self.bus = None
        self.canopen = None
        self.node = None

        self.initialized = False

        self.timeout = 1

class CommandLineTool(object):
    """docstring for CommandLineTool"""
    def __init__(self):
        super(CommandLineTool, self).__init__()
        self.running = False

        self.eds_files = [
            "/home/xaedes/gits/fahrrad/eds/605.3150.68-B-EK-2-60.eds",
            "/home/xaedes/gits/fahrrad/workspace/src/fahrrad_antrieb/src/fahrrad_antrieb/epos2.eds"
        ]

        self.can_devices = self.list_can_devices()
        self.commands = ["device","node","init","read","write","list","quit","eds"]

        self.can = CanRelated()
        self.can.can_device = self.can_devices[0]
        self.can.node_id = 1
        self.can.eds = self.eds_files[0]

        self.can_objects = [field for field in dir(Can402Objects) if not field.startswith("_")]
        print self.can_objects

        self.init_autocomplete()
        self.init_can()

    def _complete_last_arg(self, args, options):
        if not args:
            return options
        else:
            return [option for option in options if option.startswith(args[-1])]


    def complete_commands(self):
        return [cmd + " " for cmd in self.commands]

    def complete_device(self, args):
        return self._complete_last_arg(args, self.can_devices)
        
    def complete_node(self, args):
        return self._complete_last_arg(args, map(str,[1,2]))

    def complete_read(self, args):
        return self._complete_last_arg(args, self.can_objects)

    def complete_write(self, args):
        return self._complete_last_arg(args, self.can_objects)

    def complete_list(self, args):
        return []
        
    def complete_quit(self, args):
        return []

    def complete_eds(self, args):
        return self._complete_last_arg(args, self.eds_files)
        
    def commands_completer(self, text, state):
        # get already inputted text
        line_buffer = readline.get_line_buffer()

        orig_len = len(line_buffer)
        line = line_buffer.lstrip()
        stripped = orig_len - len(line)
        begidx = readline.get_begidx() - stripped
        endidx = readline.get_endidx() - stripped        

        being_completed = line[begidx:endidx]

        # print "_"+being_completed+"_"

        # print len(line), line

        line = line.split()

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
        if self.can.node is not None:
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

            for can_object in self.can_objects:
                self.can.node.init_object(*self.parse_can_object(can_object))

            self.can.node.start_thread()
            self.initialized = True
            print "CanOpen successful initialized:"
            print "\tcan device: %s" % self.can.can_device
            print "\tnode id: %d" % self.can.node_id
            print "\teds: %s" % self.can.eds

        except Exception, e:
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


    def can_object_valid(self, obj):
        return hasattr(Can402Objects, obj)
        # return obj in self.can_objects

    def parse_can_object(self, obj):
        index, subindex = getattr(Can402Objects, obj)
        return index, subindex

    def cmd_read(self, args):
        if not args or not self.parse_can_object(args[0]):
            raise ValueError()
        index, subindex = self.parse_can_object(args[0])
        read = SdoRead(self.can.node, index, subindex, timeout=self.can.timeout)
        read.start()
        read.evt_done.wait()
        if read.evt_success.isSet():
            for byte in read.result:
                print hex(byte),
            self.can.node.object_dict[(index, subindex)].update_raw_data(read.result)

            print ""
            print self.can.node.object_dict[(index, subindex)].value
            
            # print bytearray(read.result)
        elif read.evt_timeout.isSet():
            print "timeout"
        elif read.evt_fault.isSet():
            print "fault"

    def cmd_eds(self, args):
        if not args:
            raise ValueError()

        self.can.eds = args[0]
        print "Ok, set eds file to '%s'." % self.can.eds
        self.init_can()



    def cmd_init(self, args):
        self.init_can()

    def cmd_quit(self, args):
        self.running = False
        self.stop_can_node()



    def is_parseable_number(self, str):
        try:
            parseIntAutoBase(str)
            return True
        except ValueError:
            return False


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
                try:
                    impl(args)
                except ValueError:
                    raise e

                # print "Execute cmd %s" % cmd
            # print inp == self.commands_completer(inp,0)
        
def main():
    clt = CommandLineTool()
    clt.spin()
    
if __name__ == '__main__':
    main()