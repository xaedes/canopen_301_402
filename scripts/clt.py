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
        
        self.bus = None
        self.canopen = None
        self.node = None

        self.initialized = False

class CommandLineTool(object):
    """docstring for CommandLineTool"""
    def __init__(self):
        super(CommandLineTool, self).__init__()
        self.can_devices = self.list_can_devices()
        self.commands = ["device","node","read","write","list","quit"]

        self.can = CanRelated()
        self.can.can_device = self.can_devices[0]
        self.can.node_id = 1

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
        return self._complete_last_arg(args, [1,2])

    def complete_read(self, args):
        return self._complete_last_arg(args, ["Controlword","Statusword"])

    def complete_write(self, args):
        return self._complete_last_arg(args, ["Controlword","Statusword"])

    def complete_list(self, args):
        return []
        
    def complete_quit(self, args):
        return []
        
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


    def init_can(self):
        self.initialized = False
        try:
            self.can.bus = can.interface.Bus(self.can.can_device, bustype='socketcan_ctypes')
            self.can.canopen = CanOpen(self.can.bus)
            self.can.node = CanOpenNode(self.can.canopen,node_id=self.can.node_id)
            self.can.node.start_thread()
            self.initialized = True

        except Exception, e:
            raise e
    
    def list_can_devices(self):
        return ["can0","vcan0"]

    def parse(self, inp):
        words = [word.strip() for word in inp.lstrip().split()]
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

    def cmd_read(self, args):
        pass

    def spin(self):
        while True:
            print self.can.__dict__
            inp = raw_input("> ")
            print "You entered '%s'" % inp
            
            cmd, args = self.parse(inp)
            print "cmd, args:", cmd, args

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