
from canopen_301_402.operations.operation import *
from time import sleep
import mock

evt_done_timeout = 2.0

TRACE = True

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

    foo = "bar"

    class Testclass(AsyncOperation):
        def __init__(self):
            super(Testclass, self).__init__(node=node)
        
        def process_msg(self, msg):
            if msg == foo:
                self.on_success()

    foo = Testclass()
    foo.start()
    foo.process_msg(foo)
    foo.evt_done.wait(evt_done_timeout)

    assert foo.evt_success.isSet()
    assert not foo.evt_fault.isSet()
    assert not foo.evt_timeout.isSet()
    
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

def test_send():
    global evt_done_timeout
    
    factory = mock.MagicMock()
    node = mock.MagicMock()

    async_send = AsyncSend(node,factory)
    async_send.start()
    async_send.evt_done.wait(evt_done_timeout)

    factory.assert_called_once_with()
    msg = factory.return_value
    node.canopen.send.assert_called_once_with(msg)

def test_send_and_await():
    global evt_done_timeout

    factory = mock.MagicMock()
    node = mock.MagicMock()

    predicate = lambda _: True

    async_send_and_await = AsyncSendAndAwait(node,factory,predicate)
    async_send_and_await.start()

    factory.assert_called_once_with()
    msg = factory.return_value
    node.canopen.send.assert_called_once_with(msg)

    async_send_and_await.process_msg(msg)
    async_send_and_await.evt_done.wait(evt_done_timeout)

    assert async_send_and_await.evt_success.isSet()
    assert not async_send_and_await.evt_fault.isSet()
    assert not async_send_and_await.evt_timeout.isSet()


def test_sdo_write_success():
    global evt_done_timeout

    node = mock.MagicMock()
    index,subindex = 1,2
    data = [3,4]
    
    write = SdoWrite(node,index,subindex,data)
    write.start()

    assert node.canopen.send.called

    msg, = node.canopen.send.call_args[0]
    assert type(msg) == CanOpenMessageSdoWriteRequest

    response = CanOpenMessageSdoWriteResponse(node.canopen, node.node_id, index, subindex)

    write.process_msg(response)

    write.evt_done.wait(evt_done_timeout)

    assert write.evt_success.isSet()
    assert not write.evt_fault.isSet()
    assert not write.evt_timeout.isSet()

def test_sdo_write_fault():
    global evt_done_timeout

    node = mock.MagicMock()
    index,subindex = 1,2
    data = [3,4]
    
    write = SdoWrite(node,index,subindex,data)
    write.start()

    assert node.canopen.send.called

    msg, = node.canopen.send.call_args[0]
    assert type(msg) == CanOpenMessageSdoWriteRequest
    response = CanOpenMessageSdoError(node.canopen, node.node_id, index, subindex, 0)

    write.process_msg(response)

    write.evt_done.wait(evt_done_timeout)

    assert write.evt_fault.isSet()
    assert not write.evt_success.isSet()
    assert not write.evt_timeout.isSet()

def test_sdo_read_success():
    global evt_done_timeout

    node = mock.MagicMock()
    index,subindex = 1,2
    
    data = [3,4]
    
    read = SdoRead(node,index,subindex)
    read.start()

    assert node.canopen.send.called

    msg, = node.canopen.send.call_args[0]
    assert type(msg) == CanOpenMessageSdoReadRequest
    response = CanOpenMessageSdoReadResponse(node.canopen, node.node_id, index, subindex, data)

    read.process_msg(response)

    read.evt_done.wait(evt_done_timeout)

    assert read.evt_success.isSet()
    assert not read.evt_fault.isSet()
    assert not read.evt_timeout.isSet()

    assert read.result == data

def test_sdo_read_fault():
    global evt_done_timeout

    node = mock.MagicMock()
    index,subindex = 1,2
    data = [3,4]
    
    read = SdoRead(node,index,subindex)
    read.start()

    assert node.canopen.send.called

    msg, = node.canopen.send.call_args[0]
    assert type(msg) == CanOpenMessageSdoReadRequest
    response = CanOpenMessageSdoError(node.canopen, node.node_id, index, subindex, 0)

    read.process_msg(response)

    read.evt_done.wait(evt_done_timeout)

    assert read.evt_fault.isSet()
    assert not read.evt_success.isSet()
    assert not read.evt_timeout.isSet()
