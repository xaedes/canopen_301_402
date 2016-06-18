#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from funcy import partial

from canopen_301_402.constants import *

from canopen_301_402.canopen_301.obj_dict import CanOpenObjectDictionary
from canopen_301_402.canopen_402.can402 import CanOpen402
from canopen_301_402.canopen_301.eds import *

from canopen_301_402.canopen_301.nmt import CanOpenNetworkManagement
from canopen_301_402.canopen_301.sdo import CanOpenSdoTransfer
from canopen_301_402.canopen_301.pdo import CanOpenPdoTransfer
from canopen_301_402.canopen_301.connection_set import ConnectionSet

class CanOpenNode(object):
    def __init__(self, canopen, node_id, eds_filename=None):
        super(CanOpenNode, self).__init__()
        self.canopen = canopen
        self.node_id = node_id

        # load eds file containing application specific profile
        self.eds = EdsFile()
        if eds_filename is not None:
            self.eds.read(eds_filename)

        # set up predefined connection set, mapping canopen services to function codes
        self.connection_set = ConnectionSet()
        self.connection_set.setup_from_eds(self.eds)

        # initialize services
        self.nmt = CanOpenNetworkManagement(self)
        self.sdo = CanOpenSdoTransfer(self)
        self.pdo = CanOpenPdoTransfer(self)

        # object dictionary
        self.obj_dict = CanOpenObjectDictionary(self)

        self.state = Can301State.initialisation

        self.can402 = CanOpen402(self)
        
        
        # setup routing to services
        self.services = dict()
        self.services[CanOpenService.nmt] = self.nmt
        self.services[CanOpenService.nmt_error_control] = self.nmt
        self.services[CanOpenService.sdo_tx] = self.sdo
        self.services[CanOpenService.sdo_rx] = self.sdo
        self.services[CanOpenService.pdo1_tx] = self.pdo
        self.services[CanOpenService.pdo1_rx] = self.pdo
        self.services[CanOpenService.pdo2_tx] = self.pdo
        self.services[CanOpenService.pdo2_rx] = self.pdo
        self.services[CanOpenService.pdo3_tx] = self.pdo
        self.services[CanOpenService.pdo3_rx] = self.pdo
        self.services[CanOpenService.pdo4_tx] = self.pdo
        self.services[CanOpenService.pdo4_rx] = self.pdo
        self.services[CanOpenService.sync] = None # todo
        self.services[CanOpenService.emergency] = None # todo


