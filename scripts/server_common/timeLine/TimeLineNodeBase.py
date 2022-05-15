# -*- coding: utf-8 -*-

class TimeLineNodeBase:
    def __init__(self, timeStamp):
        self.runTimeStamp = timeStamp
        self.priority = None
        self.nodeId = 0
        self.owneTimeLine = None

    def run(self):
        print("TimeLineNodeBase.run") 

    def OnDestory(self):
        self.owneTimeLine = None

    def OnSetTimeLine(self):
        pass
