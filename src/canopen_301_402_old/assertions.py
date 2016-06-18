#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from canopen_301_402.constants import *

class Assertions():
    '''
    @summary: Collection of assertions to assert correct data and value sizes
    '''

    @classmethod
    def assert_can_id(cls, can_id):
        '''
        @summary:  asserts can_id has at most 11 bits
        @param cls:
        @param can_id:
        @result: True|False
        '''
        assert (can_id >> 11) == 0

    @classmethod
    def assert_data(cls, data, maximum_len=8):
        '''
        @summary:  asserts data contains at most maximum_len bytes
        @param cls:
        @param function_code:
        @result: True|False
        '''
        assert 0 <= len(data) <= maximum_len
    
    @classmethod
    def assert_function_code(cls, function_code):
        '''
        @summary:  asserts function_code has at most 4 bits
        @param cls:
        @param function_code:
        @result: True|False
        '''
        assert (function_code >> 4) == 0 

    @classmethod
    def assert_node_id(cls, node_id):
        '''
        @summary:  asserts node_id has at most 7 bits
        @param cls:
        @param node_id:
        @result: True|False
        '''
        assert (node_id >> 7) == 0

    @classmethod
    def assert_index(cls, index):
        '''
        @summary:  asserts index has at most 16 bits
        @param cls:
        @param index:
        @result: True|False
        '''
        assert (index >> 16) == 0

    @classmethod
    def assert_subindex(cls, subindex):
        '''
        @summary:  asserts subindex has at most 8 bits
        @param cls:
        @param subindex:
        @result: True|False
        '''
        assert (subindex >> 8) == 0

    @classmethod
    def assert_nmt_command(cls, command):
        '''
        @summary:  asserts subindex has at most 8 bits
        @param cls:
        @param subindex:
        @result: True|False
        '''
        assert command in Can301StateCommand
