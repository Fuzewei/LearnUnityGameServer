# -*- coding: utf-8 -*-
import KBEngine
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
        self.clientMoveReciveTime = 0
        self.serverMoveReciveTime = 0
        pass

    def onServerMovetimer(self, tid, *args):
        self.moveType = 0
        print("onServerMovetimer",tid)
        self.allClients.confirmMoveTimeStamp(self.clientMoveReciveTime)
    
    #服务端主动设置位置，客户端要调整
    def setAvatarMoveState(self, moveType):
        self.moveType = moveType
        self.clientMoveReciveTime = self.clientMoveReciveTime + time.time() - self.serverMoveReciveTime
        self.serverMoveReciveTime = time.time()
        self.allClients.confirmMoveTimeStamp(self.clientMoveReciveTime)

        self.addTimerCallBack(1, 0, self.onServerMovetimer)


	# 客户端定期上传位置
    def updatePosition(self, exposed, timeStamp, position, faceDirection, moveDirection):
        if timeStamp <=self.clientMoveReciveTime:
            return
        self.clientMoveReciveTime = timeStamp
        self.serverMoveReciveTime = time.time()
        self.position = position
        self.direction = faceDirection #面朝的方向
        self.moveDirection = moveDirection  #移动方向（局部）
        self.allClients.confirmMoveTimeStamp(self.clientMoveReciveTime)

    def setPostionAndRotation(self, exposed, position, faceDirection, moveDirection):
        self.position = position
        self.direction = faceDirection
        self.moveDirection = moveDirection  #移动方向（局部）
       

    def updateMovetype(self, exposed, timeStamp, moveType):
        self.clientMoveReciveTime = timeStamp
        self.serverMoveReciveTime = time.time()
        self.moveType = moveType
        self.allClients.confirmMoveTimeStamp(self.clientMoveReciveTime)

    def setInBattle(self, exposed, timeStamp, inbattle):
        self.clientMoveReciveTime = timeStamp
        self.serverMoveReciveTime = time.time()
        self.inbattle = inbattle
        self.allClients.confirmMoveTimeStamp(self.clientMoveReciveTime)


	#移动状态改变
    def updateAvatarMoveState(self, exposed, timeStamp, moveType, position, faceDirection, moveDirection, inbattle):
        if self.moveType == 6 and self.moveType != moveType:
            return
        if moveType == 6 and self.moveType != 6:
            return

        self.clientMoveReciveTime = timeStamp
        self.serverMoveReciveTime = time.time()
        self.moveType = moveType
        self.position = position
        self.direction = faceDirection
        self.moveDirection = moveDirection  #移动方向（局部）
        self.setInBattle(inbattle)
        self.allClients.confirmMoveTimeStamp(self.clientMoveReciveTime)
