#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from funcy import partial

from canopen_301_402.constants import *
from canopen_301_402.async.async_chain import AsyncChain
from canopen_301_402.async.async_send import AsyncSend
from canopen_301_402.async.async_send_and_await import AsyncSendAndAwait
from canopen_301_402.canopen_msgs.msgs import CanOpenMessageNmtCommand
from canopen_301_402.canopen_msgs.msgs import CanOpenMessageNmtBootup
from canopen_301_402.can402.ops.change_state import ChangeState
from canopen_301_402.can402.ops.set_mode import SetMode

class Init(AsyncChain):
    """docstring for Init"""
    def __init__(self, node, *args, **kwargs):
        self.node = node

        reset_communication = partial(AsyncSendAndAwait,
                                node = node,
                                send_msg_factory = partial(
                                                        CanOpenMessageNmtCommand, 
                                                        self.node.canopen, self.node.node_id, Can301StateCommand.reset_communication),
                                await_msg_predicate = lambda msg: (type(msg)==CanOpenMessageNmtBootup),
                                timeout = self.node.atomic_timeout)

        start_remote_node   = partial(AsyncSend,
                                node = node,
                                send_msg_factory = partial(
                                                        CanOpenMessageNmtCommand, 
                                                        self.node.canopen, self.node.node_id, Can301StateCommand.start_remote_node),
                                timeout = self.node.atomic_timeout)

        shutdown            = partial(ChangeState, node=node, command=Can402StateCommand.shutdown,         timeout = self.node.atomic_timeout)
        switch_on           = partial(ChangeState, node=node, command=Can402StateCommand.switch_on,        timeout = self.node.atomic_timeout)
        enable_operation    = partial(ChangeState, node=node, command=Can402StateCommand.enable_operation, timeout = self.node.atomic_timeout)

        operations = [reset_communication, start_remote_node, shutdown, switch_on, enable_operation]

        super(Init, self).__init__(node, operations, *args, **kwargs)
        
