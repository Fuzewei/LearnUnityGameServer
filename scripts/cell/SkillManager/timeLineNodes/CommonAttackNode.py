# -*- coding: utf-8 -*-
from SkillManager.timeLineNodes import SkillNodeBase 

class CommonAttackNode(SkillNodeBase):
    def __init__(self, timeStamp):
        SkillNodeBase.__init__(self, timeStamp)


    #客户端发来的信息
    def clientCall(self, args):
        pass
    
    #Node到运行的时间点了
    def run(self):
        SkillNodeBase.run(self)

