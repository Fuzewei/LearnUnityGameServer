# -*- coding: utf-8 -*-
from SkillManager.timeLineNodes.SkillNodeBase import SkillNodeBase 
from Const.MoveState import SERVER_MOVING_STAGE
from Const.MoveState import CLIENT_MOVE_CONST
import KBEngine


class CommonAttackNode(SkillNodeBase):
    _hitEntity = -1
    def __init__(self, timeStamp):
        SkillNodeBase.__init__(self, timeStamp)

   #客户端发来的信息(命中信息)
    def clientCall(self, exposed, args):
        self.hitEntity(args)
          
    def hitEntity(self, args):
        entityId = int(args[0])
        entity = KBEngine.entities.get(entityId)
        entity.startP3ClientMove(self.avatarOwner.id, 1)
        self.owneTimeLine.callAllClient(args)


    #命中的客户端上传信息
    def updateEntityPosition(self, args):

        pass

    #Node到运行的时间点了
    def run(self):
        SkillNodeBase.run(self)

