#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from funcy import partial

from canopen_301_402.constants import *
from canopen_301_402.async.async_chain import AsyncChain
from canopen_301_402.async.async_send_and_await import AsyncSendAndAwait
from canopen_301_402.canopen_msgs.msgs import CanOpenMessageNmtCommand
from canopen_301_402.canopen_msgs.msgs import CanOpenMessageNmtBootup
from canopen_301_402.can402.ops.change_state import ChangeState

class Quit(AsyncChain):
    """docstring for Quit"""
    def __init__(self, node, *args, **kwargs):
        self.node = node

        shutdown            = partial(ChangeState, node=node, command=Can402StateCommand.shutdown)

        reset_communication = partial(AsyncSendAndAwait,
                                node = node,
                                send_msg_factory = partial(
                                                        CanOpenMessageNmtCommand, 
                                                        self.node.canopen, self.node.node_id, Can301StateCommand.reset_communication),
                                await_msg_predicate = lambda msg: (type(msg)==CanOpenMessageNmtBootup))

        operations = [shutdown, reset_communication]

        super(Quit, self).__init__(node, operations, *args, **kwargs)        
