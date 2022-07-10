# -*- coding: utf-8 -*-
from SkillManager.timeLineNodes.SkillNodeBase import SkillNodeBase 
from Const.MoveState import SERVER_MOVING_STAGE
from Const.MoveState import CLIENT_MOVE_CONST
import KBEngine


class CommonAttackNode(SkillNodeBase):
    _hitEntity = -1
    def __init__(self, timeStamp):
        SkillNodeBase.__init__(self, timeStamp)
        self.hitFlyDurationTime = 1.0

   #客户端发来的信息(命中信息)
    def clientCall(self, exposed, args):
        entityId = int(args[0])
        entity = KBEngine.entities.get(entityId)
        tid = self.avatarOwner.addTimerCallBack(self.hitFlyDurationTime, 0, self.onTimeBeStrikefly, entityId)
        entity.switch2BeStrikefly(self.avatarOwner.id, tid) #进入被击飞状态
        #entity.startP3ClientMove(self.avatarOwner.id)
        self.owneTimeLine.callAllClient(self.nodeId, args)
        print("CommonAttackNode:clientCall", exposed, self.avatarOwner.id, args)
          
    #Node到运行的时间点了
    def run(self):
        SkillNodeBase.run(self)

    def onTimeBeStrikefly(self, tid, entityId):
        entity = KBEngine.entities.get(entityId)
        #entity.stopP3ClientMove()
        entity.strikeflyDone(tid)
        entity.switch2Idle()
        pass

