#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import can

def set_timeout(timeout,callback):
    '''
    @summary: calls a function after a specified number of seconds
    @param timeout: number of seconds
    @param callback: function be called 
    @result: 
    '''
    pass # TODO

def collect_all_leaf_subclasses(Type):
    '''
    @summary: returns a list of classes that inherit from type and have no further inheriting subclasses
    @param Type: new style class type
    @result: list of classes
    '''

    # current subclasses
    subclasses = Type.__subclasses__()

    # no further inheriting subclasses; Type is part of result
    if len(subclasses) == 0:
        return [Type]
    else:
        # this type is no leaf type
        # look for further inheriting subclasses
        # and collect their leaf subclasses
        result = list()
        for subclass in subclasses:
            result.extend(collect_all_leaf_subclasses(subclass))
        return result

def parseIntAutoBase(string):
    if string is None: return None
    string = string.strip()

    # if it is a negative number the prefix starts after the minus sign
    # use a variable offset where the prefix should start
    if string[0] == "-":
        offset = 1
    else:
        offset = 0

    if string[offset:][:2] == "0x":
        base = 16
    elif string[offset:][:2] == "0o":
        base = 8
    elif string[offset:][:2] == "0b":
        base = 2
    else:
        base = 10

    return int(string,base)


class HistoryListener(can.Listener):
    def __init__(self):
        self.msgs = list()
    def on_message_received(self,msg):
        self.msgs.append(msg)
        
def str_to_can_msg(string):
    '''
    @summary:      Converts string to can.Message
    @param string: has same format as linux tool "cansend". e.g. '601#01.01.01.01'
    @result:      can.Message
    '''

    # remove not allowed characters
    allowed = "0123456789.#RABCDEF"
    string = string.upper()
    string = ''.join([char for char in string if char in allowed])

    hashidx = string.index("#")
    head = string[:hashidx]
    body = string[hashidx+1:]


    arb_id = int(head,16)
    if body == "R":
        data = []
        req = True    
    else:
        data = body.split(".")
        data = [int(item,16) for item in data]
        req = False

    msg = can.Message(extended_id=False,arbitration_id=arb_id,data=data,is_remote_frame=req)

    return msg



def can_msg_to_str(msg):
    '''
    @summary: Converts can.Message to string
    @param msg: can.Message
    @result:    has same format as linux tool "cansend". e.g. '601#01.01.01.01'
    '''
    head = hex(msg.arbitration_id)[2:]
    if msg.is_remote_frame:
        body = "R"
    else:
        body = []
        for byte in msg.data:
            str_byte = hex(byte)[2:]
            if len(str_byte) < 2:
                str_byte = ((2-len(str_byte)) * "0") + str_byte
                body.append(str_byte)
        
        body = ".".join(body)

    result = (head+"#"+body).upper()
    return result

