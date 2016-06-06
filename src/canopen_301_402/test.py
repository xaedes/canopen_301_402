#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import can

from canopen_301_402.canopen import CanOpen,eds_config
from canopen_301_402.constants import *

bus = can.interface.Bus('vcan0', bustype='socketcan_ctypes')
canopen=CanOpen(bus,eds_config)

msg = canopen.msgs.nmt(1,Can301StateCommand.start_remote_node)
# msg = canopen.msgs.nmt_request()
# msg = canopen.msgs.sdo_write_request(node_id=1, index=0x6040, subindex=0x00, data=[0x00,0x00])
# msg = canopen.msgs.sdo_write_request(node_id=1, index=0x6040, subindex=0x00, data=[0x06,0x00])
# msg = canopen.msgs.sdo_read_request(node_id=1, index=0x6041, subindex=0x00)
canopen.send_msg(msg)

while True:
    pass
