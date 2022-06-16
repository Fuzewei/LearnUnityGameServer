# -*- coding: utf-8 -*-
from SkillManager.timeLineNodes.SkillNodeBase import SkillNodeBase 
from Const.MoveState import SERVER_MOVING_STAGE 

class PlayerAnimationNode(SkillNodeBase):
    def __init__(self, timeStamp, name):
        SkillNodeBase.__init__(self, timeStamp)
        self.animName = name
        
    #客户端发来的信息
    def clientCall(self, exposed, args):
        pass
    
    #Node到运行的时间点了
    def run(self):
        SkillNodeBase.run(self)
