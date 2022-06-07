# -*- coding: utf-8 -*-
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
        self.clientMoveReciveTime = 0 #客户端移动接收时间
        self.serverMoveReciveTime = 0



        self.serverMoveTimer = 0
        self.updatePositionClientId = self.id #接受上传位置的客户端id
      


    def onServerMovetimer(self, tid, finishMoveState):
        print("onServerMovetimer",tid)
        self.serverMoveTimer = 0
        self.stopP3ClientMove(finishMoveState)
        self.allClients.confirmMoveTimeStamp(self.clientMoveReciveTime)
 

    #开启p3控制的移动(怪物放技能，怪物击退，人物击退)也就是设置按照某一端的位置同步所有的客户端
    def startP3ClientMove(self, controlId, durTime):
        self.updatePositionClientId = controlId
        self.moveType = CLIENT_MOVE_CONST.ServerMove
        self.allClients.startP3ClientMove(time.time() - self.baseTime, controlId)
        self.serverMoveTimer = self.addTimerCallBack(durTime, 0, self.onServerMovetimer, CLIENT_MOVE_CONST.Idel)

    #结束p3控制的移动(怪物放技能，怪物击退，人物击退)也就是设置按照某一端的位置同步所有的客户端
    def stopP3ClientMove(self, moveStage):
        self.updatePositionClientId = self.id
        self.moveType = moveStage
        self.allClients.stopP3ClientMove(time.time() - self.baseTime)
        
        

    # p3户端tick上传位置
    def p3UpdatePosition(self, exposed, timeStamp, position, faceDirection, moveDirection):
        if exposed != self.updatePositionClientId:
            return
        self.clientMoveReciveTime = timeStamp
        self.serverMoveReciveTime = time.time()
        self.position = position
        self.direction = faceDirection #面朝的方向
        self.moveDirection = moveDirection  #移动方向（局部）
        self.allClients.confirmMoveTimeStamp(self.clientMoveReciveTime)



	# 主客户端上传位置
    def updatePosition(self, exposed, timeStamp, position, faceDirection, moveDirection):
        if exposed != self.updatePositionClientId:
            return
        self.clientMoveReciveTime = timeStamp
        self.serverMoveReciveTime = time.time()
        self.position = position
        self.direction = faceDirection #面朝的方向
        self.moveDirection = moveDirection  #移动方向（局部）
        self.allClients.confirmMoveTimeStamp(self.clientMoveReciveTime)





    # 客户端上传怪物的位置
    def setPostionAndRotation(self, exposed, position, faceDirection, moveDirection):
        self.position = position
        self.direction = faceDirection
        self.moveDirection = moveDirection  #移动方向（局部）
        self.allClients.confirmMoveTimeStamp(time.time() - self.baseTime)
       

    def updateMovetype(self, exposed, timeStamp, moveType):
        self.clientMoveReciveTime = timeStamp
        self.serverMoveReciveTime = time.time()
        self.moveType = moveType
        self.allClients.confirmMoveTimeStamp(self.clientMoveReciveTime)

    def setInBattle(self, exposed, timeStamp, inbattle):
        self.clientMoveReciveTime = timeStamp
        self.serverMoveReciveTime = time.time()
        print("setInBattle",inbattle)
        self.inBattle = inbattle
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
