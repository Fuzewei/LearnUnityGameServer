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
        pass

	# 客户端定期上传位置
    def updatePosition(self, exposed, timeStamp, position, faceDirection, moveDirection):
        self.position = position
        self.direction = faceDirection #面朝的方向
        self.moveDirection = moveDirection  #移动方向（局部）
        self.allClients.confirmMoveTimeStamp(timeStamp)

	#移动状态改变
    def updateAvatarMoveState(self, exposed, timeStamp, moveType, position, faceDirection, moveDirection, inbattle):
        self.moveType = moveType
        self.position = position
        self.direction = faceDirection
        self.moveDirection = moveDirection  #移动方向（局部）
        self.setInBattle(inbattle)
        self.allClients.confirmMoveTimeStamp(timeStamp)
