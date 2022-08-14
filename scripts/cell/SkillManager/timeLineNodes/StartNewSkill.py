# -*- coding: utf-8 -*-
from SkillManager.timeLineNodes.SkillNodeBase import SkillNodeBase 

class StartNewSkill(SkillNodeBase):
    def __init__(self, nodeInfo):
        SkillNodeBase.__init__(self, nodeInfo)
        # self.durationTime = _durationTime
        # self.newSkillId = _newSkillId

    
    #客户端发来的信息
    def clientCall(self, exposed, args):
        self.owneTimeLine.callAllClient(args)
    
    #Node到运行的时间点了
    def run(self):
        SkillNodeBase.run(self)
