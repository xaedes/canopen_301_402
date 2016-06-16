#!/usr/bin/env python2
# -*- coding: utf-8 -*-

class Signal(object):
    def __init__(self):
        super(Signal, self).__init__()
        self.callbacks = list()
        self.callbacks_once = list()

    def register(self, callback):
        self.callbacks.append(callback)

    def register_once(self, callback):
        self.callbacks_once.append(callback)

    def unregister(self, callback):
        if callback in self.callbacks: self.callbacks.remove(callback)
        if callback in self.callbacks_once: self.callbacks_once.remove(callback)

    def dispatch(self, *args, **kwargs):
        callbacks = list()
        for callback in self.callbacks:
            callbacks.append(callback)

        while len(self.callbacks_once) > 0:
            callback = self.callbacks_once.pop()
            callbacks.append(callback)
        
        for callback in callbacks:
            callback(*args, **kwargs)

