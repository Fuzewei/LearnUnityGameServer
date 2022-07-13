# -*- coding: utf-8 -*-
import time
import random
import Math
import KBEngine
from Utils.Quaternion import Quaternion
import Utils.Utils as Utils

class AiSMoveBase():

    def __init__(self, _moveType, entityId):
        self.moveType = _moveType #移动类型
        self.srcEntityId = entityId #所属entityId
        self.beginTime = 0 #做出新移动决定的时间
        
    #获取移动目标点
    def getMovePoint(self):
        assert(False)
    
        
    @property
    def avatar(self):
        return KBEngine.entities.get(self.srcEntityId)
    
    @property
    def enemy(self):
        return KBEngine.entities.get(self.avatar.targetID)


class AiSMoveWalk(AiSMoveBase):

    def __init__(self, _moveType, entityId):
        super(AiSMoveWalk, self).__init__(_moveType, entityId)
        self.tarPoint = None #移动目标点
       
    def getMovePoint(self):
        avatarPosition = self.avatar.position
        if self.tarPoint:
            deltTime = time.time() - self.beginTime 
            dis = avatarPosition.distTo(self.tarPoint)
            if deltTime < 1.0: #前后两次时间很短
                return self.tarPoint
            if dis > 3 and random.random() < 0.7: #离玩家远，30概率重新选择位置点
                return self.tarPoint 
        self.beginTime = time.time()
        self.tarPoint = self.calcNewPoint()
        return self.tarPoint
    
    def calcNewPoint(self):
        enemyPosition = self.enemy.position
        distance = self.avatar.position.distTo(enemyPosition)
        enemyDirection = self.avatar.position - enemyPosition
        enemyDirection.y = 0
        enemyDirection.normalise()
        
        angles = [-30,  -20, -10,  -5,   0,   5,  10,  20,  30]
        weights = [2,   4,    6,   19,   22,  10,  6,  4,    2]
        angle = Utils.RandonChoice(angles, weights)
        lens =   [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
        weights = [1, 2 , 4 , 5,  6,  5 , 4,  2 , 1]
        len = Utils.RandonChoice(lens, weights)
        quat = Quaternion.axisAngle(Math.Vector3(0.0, 1.0, 0.0), angle)
        direction = quat.multiVec3(enemyDirection)
        desPoint = enemyPosition + direction * len

        desPoint = self.avatar.getRandomPoints(desPoint, 0.5, 1, 0)[0]
        return desPoint

    
#ai战斗移动决策
class AiMoveDecision():
    
    moveCls = {
        1 : AiSMoveWalk,
    }

    def __init__(self, entityId):
        self.srcEntityId = entityId
        self.lastMoveDecision = None
        
    def getMovePoint(self, moveType):
        position = None
        if moveType not in AiMoveDecision.moveCls:
            #todo : 自动选择合适的对峙移动类型
            assert(False)
        if not self.lastMoveDecision or self.lastMoveDecision.moveType != moveType:
            self.lastMoveDecision = AiMoveDecision.moveCls[moveType](moveType, self.srcEntityId)
            position = self.lastMoveDecision.getMovePoint()
        else:
            position = self.lastMoveDecision.getMovePoint()
        return position 
    
    @property
    def avatar(self):
        return KBEngine.entities.get(self.srcEntityId)
    