
import threading

from brave_new_world.canopen_msgs.msgs import *
from brave_new_world.constants import *

def set_timeout(time, callback):
    timer = threading.Timer(time, callback)
    timer.start()

class AsyncOperation(object):
    """docstring for AsyncOperation"""
    def __init__(self, node, timeout=None):
        super(AsyncOperation, self).__init__()
        self.node = node
        self.canopen = node.canopen
        self.timeout = timeout
        self.timeout_timer = None


        self.evt_done = threading.Event()
        self.evt_success = threading.Event()
        self.evt_timeout = threading.Event()
        self.evt_fault = threading.Event()

    def _on_timeout(self):
        self.evt_timeout.set()
        self.evt_done.set()

    def start(self):
        if self.timeout is not None:
            self.timeout_timer = threading.Timer(self.timeout, self._on_timeout)
            self.timeout_timer.start()
        else:
            self.timeout_timer = None

        self.node.current_operations.append(self)
        self.do()

        # try:
        #     self.do()
        #     self.evt_success.set()
        # except:
        #     self.evt_fault.set()
        # finally:
        #     self.evt_done.set()

    def do(self):
        pass
        
    def process_msg(self, msg):
        return False

    def on_success(self):
        self.evt_success.set()
        self.evt_done.set()
        
    def on_fault(self):
        self.evt_fault.set()
        self.evt_done.set()
        
    def on_timeout(self):
        self.evt_timeout.set()
        self.evt_done.set()


class SdoWrite(AsyncOperation):
    """docstring for SdoWrite"""
    def __init__(self, node, index, subindex, data, *args, **kwargs):
        self.index = index
        self.subindex = subindex
        self.data = data
        super(SdoWrite, self).__init__(node, *args, **kwargs)
        
    def do(self):
        self.canopen.send(CanOpenMessageSdoWriteRequest(self.canopen, self.node.node_id, self.index, self.subindex, self.data))


    def process_msg(self, msg):
        if ((type(msg) == CanOpenMessageSdoWriteResponse)
             and (msg.index == self.index)
             and (msg.subindex == self.subindex)):

            self.on_success()
            return True
            
        elif ((type(msg) == CanOpenMessageSdoError)
             and (msg.index == self.index)
             and (msg.subindex == self.subindex)):

            self.on_fault()
            return True

class SdoRead(AsyncOperation):
    """docstring for SdoWrite"""
    def __init__(self, node, index, subindex, *args, **kwargs):
        self.index = index
        self.subindex = subindex
        self.result = None
        super(SdoRead, self).__init__(node, *args, **kwargs)
        
    def do(self):
        self.canopen.send(CanOpenMessageSdoReadRequest(self.canopen, self.node.node_id, self.index, self.subindex))


    def process_msg(self, msg):
        if ((type(msg) == CanOpenMessageSdoReadResponse)
             and (msg.index == self.index)
             and (msg.subindex == self.subindex)):

            self.result = msg.read_data
            self.on_success()
            return True


        elif ((type(msg) == CanOpenMessageSdoError)
             and (msg.index == self.index)
             and (msg.subindex == self.subindex)):

            self.on_fault()
            return True

class AsyncChain(AsyncOperation):
    """docstring for AsyncChain"""
    def __init__(self, node, operations, *args, **kwargs):
        self.node = node
        self.operations = operations

        super(AsyncChain, self).__init__(node, *args, **kwargs)

    def do(self):
        for Op in self.operations:
            op = Op()
            op.start()
            op.evt_done.wait()
            if op.evt_success.isSet():
                continue
            elif op.evt_timeout.isSet():
                self.on_timeout()
            elif op.evt_fault.isSet():
                self.on_fault()
        self.on_success()

class AsyncSend(AsyncOperation):
    """docstring for AsyncChain"""
    def __init__(self, node, send_msg_factory, *args, **kwargs):
        self.node = node
        self.send_msg_factory = send_msg_factory
        super(AsyncSend, self).__init__(node, *args, **kwargs)

    def do(self):
        msg = self.send_msg_factory()
        self.canopen.send(msg)
        self.on_success()


class AsyncSendAndAwait(AsyncOperation):
    """docstring for AsyncChain"""
    def __init__(self, node, send_msg_factory, await_msg_predicate, *args, **kwargs):
        self.node = node
        self.send_msg_factory = send_msg_factory
        self.await_msg_predicate = await_msg_predicate
        super(AsyncSendAndAwait, self).__init__(node, *args, **kwargs)

    def do(self):
        msg = self.send_msg_factory()
        self.canopen.send(msg)

    def process_msg(self, msg):
        if self.await_msg_predicate(msg):
            self.on_success()

