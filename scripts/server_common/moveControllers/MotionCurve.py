# -*- coding: utf-8 -*-
import time
import math
import Math
import KBEngine
from KBEDebug import *

# 
# 管理移动曲线的类
# 

class MotionCurve(object):

    def __init__(self, moveInfo):
        super(MotionCurve, self).__init__()
        self.moveInfo = moveInfo
        self.maxDelterTime = self.moveInfo[-1].timeStamp

    def lerpMotion(self, timeStamp):
        left = None
        right = None
        for item in self.moveInfo:
            if timeStamp >= item.timeStamp:
                left = item
                right = item
            if timeStamp <= item.timeStamp:
                right = item
        if left == None:  #左边没有
            return Math.Vector3(0,0,0)

        if right.timeStamp == left.timeStamp:  #右边没有
            return Math.Vector3(left.x, left.y, left.z)
        else:
            percent = (timeStamp - left.timeStamp) / (right.timeStamp - left.timeStamp)
            x = left.x * (1 - percent) + right.x * percent
            y = left.y * (1 - percent) + right.y * percent
            z = left.z * (1 - percent) + right.z * percent
            return Math.Vector3(x, y, z)
        

    def delterPosition(self ,oldT, newT):
        oldV = self.lerpMotion(oldT)
        newV = self.lerpMotion(newT)
        return newV - oldV

    def isEnd(self, testTime):
        return testTime >= self.maxDelterTime

