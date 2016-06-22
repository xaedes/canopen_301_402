#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import threading
import signal
import sys

import Queue

class CanOpenNode(object):
    """docstring for CanOpenNode"""
    def __init__(self, canopen, node_id):
        super(CanOpenNode, self).__init__()
        self.canopen = canopen
        self.node_id = node_id
    
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
