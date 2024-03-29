# -*- coding: utf-8 -*-
from timeLine.TimeLineNodeBase import TimeLineNodeBase 

class SkillNodeBase(TimeLineNodeBase):
    def __init__(self, nodeInfo):
        TimeLineNodeBase.__init__(self, nodeInfo.beginTime)
        self.nodeType = "Monster"

    @property
    def avatarOwner(self):
        return self.owneTimeLine.avatarOwner

    def OnDestory(self):
        TimeLineNodeBase.OnDestory(self)

    def OnSetTimeLine(self):
        pass

    #客户端发来的信息
    def clientCall(self, exposed, args):
        pass

    #Node到运行的时间点了
    def run(self):
        TimeLineNodeBase.run(self)
