# -*- coding: utf-8 -*-
from ast import If
import KBEngine
from Const.MoveState import CLIENT_MOVE_CONST
import math
import Math
import time
import random
from KBEDebug import * 

class MoveControl:
    """
    客户端移动相关处理
    """
    def __init__(self):
        self.moveType = 0
        self.confirmTime = self.serverTime() #移动同步的时间
        self.controlId = self.id #接受上传位置的客户端id
      
    def getBestClient(self):
        minLenth = float('inf')
        ans = None
        for entityId in self.enemyLog:
            entitiy = KBEngine.entities.get(entityId)
            dis =  self.position.distTo(entitiy.position)
            if dis < minLenth:
                minLenth = dis
                ans = entityId
        return ans

    #开启p3控制的移动(怪物放技能，怪物击退，人物击退)也就是设置按照某一端的位置同步所有的客户端
    def startP3ClientMove(self, _controlId = None):
        if _controlId is None:
            _controlId = self.getBestClient()
        if  _controlId != self.controlId :
            self.controlId = _controlId
            self.allClients.startP3ClientMove(self.serverTime())
        

    #结束p3控制的移动(怪物放技能，怪物击退，人物击退)也就是设置按照某一端的位置同步所有的客户端
    def stopP3ClientMove(self):
        if self.controlId != self.id:
            self.controlId = self.id
            self.allClients.stopP3ClientMove(self.serverTime())
        

    # p3户端tick上传位置
    def p3UpdatePosition(self, exposed, timeStamp, position, faceDirection, moveDirection):
        if exposed != self.controlId:
            return
        DEBUG_MSG("confirmTime :%s p3UpdatePosition: %i controllerId =%i, userarg=%s" % \
						(self.confirmTime, tuple(faceDirection)[0], tuple(faceDirection)[1], tuple(faceDirection)[2]))
        self.confirmTime = timeStamp
        self.position = position
        self.direction = faceDirection #面朝的方向
        self.moveDirection = moveDirection  #移动方向（局部）
        self.allClients.confirmMoveTimeStamp(self.confirmTime)


	# 主客户端上传位置
    def updatePosition(self, exposed, timeStamp, position, faceDirection, moveDirection):
        if exposed != self.controlId:
            return
        self.confirmTime = timeStamp
        self.position = position
        self.direction = faceDirection #面朝的方向
        self.moveDirection = moveDirection  #移动方向（局部）
        self.allClients.confirmMoveTimeStamp(self.confirmTime)

    # 客户端上传怪物的位置
    def setPostionAndRotation(self, exposed, position, faceDirection, moveDirection):
        self.position = position
        self.direction = faceDirection
        self.moveDirection = moveDirection  #移动方向（局部）
        self.allClients.confirmMoveTimeStamp(self.serverTime())
       

    def updateMovetype(self, exposed, timeStamp, moveType):
        self.confirmTime = timeStamp
        self.moveType = moveType
        self.allClients.confirmMoveTimeStamp(self.confirmTime)

    def setInBattle(self, exposed, timeStamp, inbattle):
        self.confirmTime = timeStamp 
        print("setInBattle",inbattle)
        self.inBattle = inbattle
        self.allClients.confirmMoveTimeStamp(self.confirmTime)

	#移动状态改变
    def updateAvatarMoveState(self, exposed, timeStamp, moveType, position, faceDirection, moveDirection, inbattle):
        if self.moveType == 6 and self.moveType != moveType:
            return
        if moveType == 6 and self.moveType != 6:
            return

        self.confirmTime = timeStamp
        self.moveType = moveType
        self.position = position
        self.direction = faceDirection
        self.moveDirection = moveDirection  #移动方向（局部）
        self.setInBattle(inbattle)
        self.allClients.confirmMoveTimeStamp(self.confirmTime)

    def isBeStrikefly(self):
        return self.moveType == CLIENT_MOVE_CONST.beStrikefly

    def isUseSkill(self):
        return self.moveType == CLIENT_MOVE_CONST.Skill

    
    def isClientMove(self):
        return self.controlId != self.id