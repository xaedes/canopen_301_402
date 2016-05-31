#!/usr/bin/env python2
# -*- coding: utf-8 -*-

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
