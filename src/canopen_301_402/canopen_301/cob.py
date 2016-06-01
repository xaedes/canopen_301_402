#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from canopen_301_402.assertions import Assertions

class CanOpenId():
    '''
    @summary: can open interpretation of can id:
        
        only 11 bit arbitration_id is allowed

        upper 4 bits of the 11 bit arbitration_id are the function code
        lower 7 bits of the 11 bit arbitration_id are the node_id
    '''

    @classmethod
    def decode(cls, can_id):
        '''
        @summary:  split 11 bit can_id in 4 bit function code and 7 bit node_id
        @param cls:
        @param can_id: 11 bit can_id
        @result: tuple of 4 bit function code and 7 bit node_id
        '''
        Assertions.assert_can_id(can_id)

        function_code = (can_id >> 7) & 0b1111
        node_id = can_id & 0b1111111

        return function_code, node_id

    @classmethod
    def encode(cls, function_code, node_id):
        '''
        @summary: build 11 bit can_id from 4 bit function code and 7 bit node_id
        @param cls:
        @param function_code: 4 bit function code
        @param node_id: 7 bit node_id
        @result: 11 bit can_id
        '''
        Assertions.assert_function_code(function_code)
        Assertions.assert_node_id(node_id)

        can_id = (function_code << 7) | node_id

        return can_id        
