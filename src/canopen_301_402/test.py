#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import can

from canopen_301_402.canopen import CanOpen,eds_config
from canopen_301_402.constants import *

bus = can.interface.Bus('vcan0', bustype='socketcan_ctypes')
canopen=CanOpen(bus,eds_config)

msg = canopen.msgs.nmt(0,Can301StateCommand.enter_pre_operational)
canopen.send_msg(msg)