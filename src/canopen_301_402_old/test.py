#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import can

from canopen_301_402.canopen import CanOpen,eds_config
from canopen_301_402.constants import *
from canopen_301_402.canopen_msgs.msgs import *

bus = can.interface.Bus('vcan0', bustype='socketcan_ctypes')
canopen=CanOpen(bus,eds_config)

# msg = canopen.msgs.nmt(1,Can301StateCommand.start_remote_node)
msg = CanOpenMessageNmtCommand(canopen,1,Can301StateCommand.start_remote_node)
# msg = CanOpenMessageNmtCommand(canopen,1,Can301StateCommand.start_remote_node)
# msg = canopen.msgs.nmt_request()
# msg = canopen.msgs.sdo_write_request(node_id=1, index=0x6040, subindex=0x00, data=[0x00,0x00])
# msg = canopen.msgs.sdo_write_request(node_id=1, index=0x6040, subindex=0x00, data=[0x06,0x00])
# msg = canopen.msgs.sdo_read_request(node_id=1, index=0x6041, subindex=0x00)
canopen.send_msg(msg)

node = canopen.get_node(1)

def callback(*args):
	print "signal_write_complete"
	print args	


def test_sdo_write():
	bus = can.interface.Bus('vcan0', bustype='socketcan_ctypes')
	canopen=CanOpen(bus,eds_config)
	node = canopen.get_node(1)


node.sdo.signal_write_complete[Can402Objects.controlword].register(callback)

msg = CanOpenMessageSdoWriteRequest(canopen,1,Can402Objects.controlword[0],Can402Objects.controlword[1],[0x06,0x00])
canopen.send_msg(msg)

msg = CanOpenMessageSdoWriteResponse(canopen,1,Can402Objects.controlword[0],Can402Objects.controlword[1])
canopen.send_msg(msg)

while True:
    pass
