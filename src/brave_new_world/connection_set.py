#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from brave_new_world.constants import *

class ConnectionSet(object):
    '''
    @summary: opencan 2.a services 
    '''
    
    def __init__(self):
        super(ConnectionSet, self).__init__()
        self.function_codes = CanOpenPredefinedConnectionSet.copy()
    
    def setup_from_eds(self, eds):
        pass
        # todo: use eds file info to set app specific connection set

    def determine_service(self, function_code, node_id):
        if node_id == 0:
            # must be some broadcast service (i.e. nmt or sync)
            for service in CanOpenBroadcastServices:
                if function_code == self.function_codes[service]:
                    return service
        else:
            for service in CanOpenService:
                # skip broadcast services
                if service in CanOpenBroadcastServices: 
                    continue

                if function_code == self.function_codes[service]:
                    return service
        
        # nothing found
        return None

    def determine_function_code(self, service):
        return self.function_codes[service]
