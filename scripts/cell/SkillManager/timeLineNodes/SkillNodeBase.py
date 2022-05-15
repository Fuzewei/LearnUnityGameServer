# -*- coding: utf-8 -*-
from timeLine.TimeLineNodeBase import TimeLineNodeBase 

class SkillNodeBase(TimeLineNodeBase):
    def __init__(self, timeStamp):
        TimeLineNodeBase.__init__(self, timeStamp)
        self.nodeType = 1

    def run(self):
        TimeLineNodeBase.run(self)

    def OnDestory(self):
        TimeLineNodeBase.OnDestory(self)

    def OnSetTimeLine(self):
        pass

    #客户端发来的信息
    def clientCall(self, args):
        pass
