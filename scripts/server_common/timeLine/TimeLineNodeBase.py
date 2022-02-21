# -*- coding: utf-8 -*-

class TimeLineNodeBase:
    def __init__(self, timeStamp):
        self.runTimeStamp = timeStamp
        self.priority = None
        self.nodeId = 0
        self.owneTimeLine = None

    def run():
        print("TimeLineNodeBase.run") 

    def OnDestory():
        pass

    def OnSetTimeLine():
        pass
