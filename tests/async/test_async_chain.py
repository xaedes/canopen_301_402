#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from canopen_301_402.async.async_operation import AsyncOperation
from canopen_301_402.async.async_chain import AsyncChain
from time import sleep
import mock

evt_done_timeout = 2.0

TRACE = False

if TRACE:
    import hunter
    hunter.trace(module_contains="canopen_301_402")

def test_chain_success():
    global evt_done_timeout
    node = mock.MagicMock()         
    class Testclass(AsyncOperation):
        def __init__(self):
            super(Testclass, self).__init__(node=node)
        def do(self):
            self.on_success()
    
    operations=[Testclass,Testclass,Testclass,Testclass]
    chain = AsyncChain(node,operations)
    chain.start()
    chain.evt_done.wait(evt_done_timeout)

    assert chain.evt_success.isSet()

def test_chain_fail():
    global evt_done_timeout
    node = mock.MagicMock()         
    class Success(AsyncOperation):
        def __init__(self):
            super(Success, self).__init__(node=node)
        def do(self):
            self.on_success()
    class Failure(AsyncOperation):
        def __init__(self):
            super(Failure, self).__init__(node=node)
        def do(self):
            self.on_fault()
    
    operations=[Success,Success,Failure,Success]
    chain = AsyncChain(node,operations)
    chain.start()
    chain.evt_done.wait(evt_done_timeout)

    assert chain.evt_fault.isSet()
    assert not chain.evt_success.isSet()
    assert not chain.evt_timeout.isSet()


def test_chain_fail():
    global evt_done_timeout
    node = mock.MagicMock()         
    class Success(AsyncOperation):
        def __init__(self):
            super(Success, self).__init__(node=node)
        def do(self):
            self.on_success()
    class Timeout(AsyncOperation):
        def __init__(self):
            super(Timeout, self).__init__(node=node)
        def do(self):
            self.on_timeout()
    
    operations=[Success,Success,Timeout,Success]
    chain = AsyncChain(node,operations)
    chain.start()
    chain.evt_done.wait(evt_done_timeout)

    assert chain.evt_timeout.isSet()
    assert not chain.evt_success.isSet()
    assert not chain.evt_fault.isSet()
