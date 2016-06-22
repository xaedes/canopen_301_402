#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from canopen_301_402.async.async_operation import AsyncOperation
from time import sleep
import mock

evt_done_timeout = 2.0

TRACE = False

if TRACE:
    import hunter
    hunter.trace(module_contains="canopen_301_402")


def test_timeout():
    global evt_done_timeout
    timeout_time = 0.5
    sleep_time = 1.0
    

    node = mock.MagicMock()         

    class Testclass(AsyncOperation):
        def __init__(self):
            super(Testclass, self).__init__(node=node,timeout=timeout_time)
        def do(self):
            sleep(sleep_time)
    
    foo = Testclass()
    foo.start()
    foo.evt_done.wait(evt_done_timeout)

    assert foo.evt_timeout.isSet()
    assert not foo.evt_success.isSet()
    assert not foo.evt_fault.isSet()

def test_fault():
    global evt_done_timeout
    node = mock.MagicMock()         

    class Testclass(AsyncOperation):
        def __init__(self):
            super(Testclass, self).__init__(node=node)
        def do(self):
            self.on_fault()

    foo = Testclass()
    foo.start()
    foo.evt_done.wait(evt_done_timeout)

    assert foo.evt_fault.isSet()
    assert not foo.evt_success.isSet()
    assert not foo.evt_timeout.isSet()

def test_success():
    global evt_done_timeout
    node = mock.MagicMock()         

    class Testclass(AsyncOperation):
        def __init__(self):
            super(Testclass, self).__init__(node=node)
        def do(self):
            self.on_success()

    foo = Testclass()
    foo.start()
    foo.evt_done.wait(evt_done_timeout)

    assert foo.evt_success.isSet()
    assert not foo.evt_fault.isSet()
    assert not foo.evt_timeout.isSet()
    
def test_process_msg():
    global evt_done_timeout
    node = mock.MagicMock()         

    foo_msg = "bar"

    class Testclass(AsyncOperation):
        def __init__(self):
            super(Testclass, self).__init__(node=node)
        
        def process_msg(self, msg):
            if msg == foo_msg:
                self.on_success()

    foo = Testclass()
    foo.start()
    foo.process_msg(foo_msg)
    foo.evt_done.wait(evt_done_timeout)

    assert foo.evt_success.isSet()
    assert not foo.evt_fault.isSet()
    assert not foo.evt_timeout.isSet()
    

def test_current_op():
    global evt_done_timeout
    node = mock.MagicMock()         

    node.current_operations = list()

    foo = AsyncOperation(node)
    foo.start()

    assert foo in node.current_operations

    foo.on_success()
    
    assert foo not in node.current_operations

    assert foo.evt_done.isSet()
    assert foo.evt_success.isSet()
    assert not foo.evt_fault.isSet()
    assert not foo.evt_timeout.isSet()
    