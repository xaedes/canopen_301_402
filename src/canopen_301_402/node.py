#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import threading
import signal
import sys

import Queue

from collections import defaultdict

from canopen_301_402.datatypes import CanDatatypes
from canopen_301_402.obj import CanOpenObject
from canopen_301_402.eds import EdsFile

class CanOpenNode(object):
    """docstring for CanOpenNode"""
    def __init__(self, canopen, node_id):
        super(CanOpenNode, self).__init__()
        self.canopen = canopen
        self.node_id = node_id

        self.datatypes = CanDatatypes()
        self.eds = EdsFile()
        self.object_dict = defaultdict(lambda:None)
    
        self.current_operations = list()
        self.running = False
        self.thread = None

        # timeout in seconds for atomic operations
        # i.e. not chains of operations!
        self.atomic_timeout = 0.1

    def start_thread(self):
        self.running = True
        self.thread = threading.Thread(target=self.spin)

        signal.signal(signal.SIGINT, self.signal_handler)
        self.thread.start()
        # self.thread.join()

    def init_object(self, index, subindex):
        self.object_dict[(index, subindex)] = CanOpenObject(self, index, subindex)

        return self.object_dict[(index, subindex)]

    def init_objects(self, idx_subidx_list):
        for index, subindex in idx_subidx_list:
            self.init_object(index, subindex)


    def spin(self):
        while self.running:
            try:
                msg = self.canopen.msg_queues[self.node_id].get(timeout=0.1)

                for op in self.current_operations:
                    if op.process_msg(msg): 
                        # op consumed msg
                        break

                self.current_operations = [op for op in self.current_operations if not op.evt_done.isSet()]

            except Queue.Empty:
                pass

    def signal_handler(self, signal, frame):
        print('You pressed Ctrl+C!')
        if not self.running:
            sys.exit(0)
        else:
            self.running = False
