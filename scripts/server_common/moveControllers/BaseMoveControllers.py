# -*- coding: utf-8 -*-
import time
import math
import Math
import Math3D
import KBEngine
import moveControllers.MotionCurve as MotionCurve
from KBEDebug import *

# 
# 该模块根据移动方向计算移动偏移
# 
class rootMotionInfo:
    def __init__(self, x, y, z, t):
        self.x = x
        self.y = y
        self.z = z
        self.timeStamp = t

__rootMotion = {}
def getRootMotion():
    if __rootMotion:
        return __rootMotion
    moveInfo = KBEngine.open("MoveInfo/data.json")
    while True:
        name = moveInfo.readline()
        if not name:
            break
        name = name.strip("\n")
        info = moveInfo.readline()
        info = info.strip("\n")
        info =info.split(" ")
        infos = []
        for i in range(0, len(info) - 1, 4):
            x = float(info[i])
            y = float(info[i + 1])
            z = float(info[i + 2])
            t = float(info[i + 3])
            motionInfo = rootMotionInfo(x, y, z, t)
            infos.append(motionInfo)
        __rootMotion[name] = infos
    return __rootMotion

 
class MoveControllersBase(object):

    def __init__(self, owner): #会有循环引用
        super(MoveControllersBase, self).__init__()
        self.owner = owner
        self.beginTime = time.time()
        self.lastTickTime = time.time()
        self.deltaTime = 0

    @property
    def xzMoveSpeed(self):
        return self.owner.moveSpeed

    @xzMoveSpeed.setter
    def xzMoveSpeed(self, value):
        self.owner.moveSpeed = value

    @property
    def position(self):
        return self.owner.position
    
    @position.setter
    def position(self, value):
        self.owner.position = value

    @property
    def direction(self):
        return self.owner.direction
    
    @direction.setter
    def direction(self, value):
        self.owner.direction = value

    
    def reset(self):
        self.beginTime = time.time()
        self.lastTickTime = time.time()

    def tick(self):
        self.deltaTime = time.time() - self.lastTickTime
        self.lastTickTime = time.time()

    def UpdateMoveSpeed(self):
        pass

    #这里直接返回移动距离
    def calcuteDelterPosition(self):
        pass

class NormalIdleControler(MoveControllersBase):

    def __init__(self, owner):
        super(NormalIdleControler, self).__init__(owner)
        self.acc =  5.5

    def UpdateMoveSpeed(self):
        self.xzMoveSpeed = self.xzMoveSpeed - self.acc * self.deltaTime
        self.xzMoveSpeed = max(self.xzMoveSpeed, 0.0)
       
    def calcuteDelterPosition(self):
        accTime = abs(self.xzMoveSpeed) / self.acc
        accTime = min(accTime, self.deltaTime)
        l = self.xzMoveSpeed * self.deltaTime - 0.5 * self.acc * accTime * accTime
        return  Math.Vector3(0, 0, l)


class NormalWalkControler(MoveControllersBase):

    def __init__(self, owner):
        super(NormalWalkControler, self).__init__(owner)
        self.acc =  3.76
        self.maxForwardSpeed = 2.21
        #private

    @property
    def path(self):
        return self.owner.movingInfo["path"]

    @property
    def nextId(self):
        return self.owner.movingInfo["nextId"]

    @nextId.setter
    def nextId(self, value):
        self.owner.movingInfo["nextId"] = value
        

    def reset(self):
        MoveControllersBase.reset(self)
    
    def UpdateMoveSpeed(self):
        if self.xzMoveSpeed <= self.maxForwardSpeed:
            self.xzMoveSpeed = min(self.xzMoveSpeed + self.acc, self.maxForwardSpeed)
        else:
            self.xzMoveSpeed = max(self.xzMoveSpeed - self.acc, self.maxForwardSpeed)

    def calcuteDelterPosition(self):
        accTime = abs(self.maxForwardSpeed - self.xzMoveSpeed) / self.acc
        accTime = min(accTime, self.deltaTime)
        moveLen = self.xzMoveSpeed * self.deltaTime + 0.5 * self.acc * accTime * accTime
        
        if self.nextId >= len(self.path):
            return

        nextPoint = self.path[self.nextId]
        _dis = nextPoint.distTo(self.position)
        _direction = nextPoint - self.position
        _direction.normalise()

        if moveLen <= _dis:
            self.position = self.position + _direction * moveLen
        else:
            while self.nextId < len(self.path) - 1 and moveLen > _dis:
                self.nextId = self.nextId +1
                self.position = nextPoint
                moveLen -= _dis
                nextPoint = self.path[self.nextId]
                _dis = nextPoint.distTo(self.position)
                _direction = nextPoint - self.position
                _direction.normalise()

            if moveLen < _dis:

                self.position = self.position + _direction * moveLen
            else:
                self.position = nextPoint

        self.direction = _direction
        return  Math.Vector3(0, 0, moveLen)

class NormalRunControler(NormalWalkControler):

    def __init__(self, owner):
        super(NormalRunControler, self).__init__(owner)
        self.acc =  10.8
        self.maxForwardSpeed = 5.05

    def UpdateMoveSpeed(self):
        if self.xzMoveSpeed <= self.maxForwardSpeed:
            self.xzMoveSpeed = min(self.xzMoveSpeed + self.acc, self.maxForwardSpeed)

class RootMotionControler(MoveControllersBase):

    def __init__(self, owner):
        super(RootMotionControler, self).__init__(owner)
       

    def setClip(self, clipName):
        self.aniClipName = clipName
        self.timeStamp = 0
        self.curve = MotionCurve.MotionCurve(getRootMotion()[clipName])

    def reset(self):
        MoveControllersBase.reset(self)
        self.timeStamp = 0

    def UpdateMoveSpeed(self):
        self.xzMoveSpeed = 0.0

    def calcuteDelterPosition(self):
        if self.isEnd():
            return
        _deltaV = self.curve.delterPosition(self.timeStamp, self.timeStamp + self.deltaTime)
        deltaV = Math3D.rotationVector(self.direction, _deltaV)
        self.timeStamp += self.deltaTime 
        self.position = self.position + deltaV

    def isEnd(self):
        return self.curve.isEnd(self.timeStamp)
