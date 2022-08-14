# -*- coding: utf-8 -*-
from SkillManager.timeLineNodes.SkillNodeBase import SkillNodeBase 
from Const.MoveState import SERVER_MOVING_STAGE
from Const.MoveState import CLIENT_MOVE_CONST
import KBEngine


class CommonAttackNode(SkillNodeBase):
    _hitEntity = -1
    def __init__(self, nodeInfo):
        SkillNodeBase.__init__(self, nodeInfo)
        self.hitFlyDurationTime = float(nodeInfo.skillParams.get("hitFlyDurationTime",1.0))

   #客户端发来的信息(命中信息)
    def clientCall(self, exposed, args):
        entityId = int(args[0])
        entity = KBEngine.entities.get(entityId)
        tid = self.avatarOwner.addTimerCallBack(self.hitFlyDurationTime, 0, self.onTimeBeStrikefly, entityId)
        entity.switch2BeStrikefly(self.avatarOwner.id, tid) #进入被击飞状态
        entity.setRootMotionClip(None)
        self.owneTimeLine.callAllClient(self.nodeId, args)
        print("CommonAttackNode:clientCall", exposed, self.avatarOwner.id, args)
          
    #Node到运行的时间点了
    def run(self):
        SkillNodeBase.run(self)

    def onTimeBeStrikefly(self, tid, entityId):
        entity = KBEngine.entities.get(entityId)
        entity.strikeflyDone(tid)
