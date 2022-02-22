# -*- coding: utf-8 -*-
import time
import KBEngine
import SCDefine

class CallbackHolder():
    def __init__(self, id, timeout, interval, callback, args):
        self.id = id
        self.timeout = timeout
        self.interval = interval
        self.callback = callback
        self.args = args

    def __call__(self):
        args = (self.id, ) +  self.args
        self.callback(*args)

class ItimerManager():

    def __init__(self):
        super().__init__()
        self.id2Callback = {}

    def addTimerCallBack(self, timeout, interval, callback, *args):
        _id = self.addTimer(timeout, interval, SCDefine.TIMER_TYPE_CALLBACK)
        self.id2Callback[_id] = CallbackHolder(_id, timeout, interval, callback, args)
        return _id

    def delTimerCallBack(self, tid):
        if tid in self.id2Callback:
            del self.id2Callback[tid]
            self.delTimer(tid)
       

    def onTimer(self, tid, userArg):
        if SCDefine.TIMER_TYPE_CALLBACK == userArg:
            callFunc = self.id2Callback[tid]
            if callFunc.interval == 0:
                del self.id2Callback[tid]
                self.delTimer(tid)
            callFunc()
