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
    
    name = "MoveControllersBase"

    def __init__(self, owner): #会有循环引用
        super(MoveControllersBase, self).__init__()
        self.owner = owner
        assert(owner.canNavigate())
        self.beginTime = time.time()
        self.lastTickTime = time.time()
        self.deltaTime = 0
        self.clientConfirmTime = time.time()

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
    def direction(self): #是欧拉角
        return self.owner.direction
    
    @direction.setter
    def direction(self, value):
        self.owner.direction = value
        
    @property
    def moveDirection(self): #是向量
        return self.owner.moveDirection
    
    @moveDirection.setter
    def moveDirection(self, value):
        self.owner.moveDirection = value

    def reset(self):
        self.beginTime = time.time()
        self.lastTickTime = time.time()

    #心跳
    def tick(self):
        self.deltaTime = time.time() - self.lastTickTime
        self.lastTickTime = time.time()
        
    #客户端传来位置信息（服务端校验）
    def clientSetPDM(self, position, direction, moveDirection):
        if self.checkClientPosition(position, direction, moveDirection):
            self.position = position
            self.direction = direction
            self.moveDirection = moveDirection
            self.lastTickTime = time.time()
            self.clientConfirmTime = time.time()

    #校验客户端发来的信息
    def checkClientPosition(self, position, direction, moveDirection):
        INFO_MSG("checkClientPosition: controllerName = %s,  self.Pos = %s, position = %s" % (self.name ,self.position, position))
        return True

    def UpdateMoveSpeed(self):
        pass

    #这里直接返回移动距离
    def calcuteDelterPosition(self):
        pass

    #要切换了
    def onSwitch(self):
        pass
    
    #移动结束了
    def isDone(self):
        return False

class NormalIdleControler(MoveControllersBase):
    
    name = "NormalIdleControler"
    
    def __init__(self, owner):
        super(NormalIdleControler, self).__init__(owner)
        self.acc =  5.5 #停止时的加速度

    def UpdateMoveSpeed(self):
        self.xzMoveSpeed = self.xzMoveSpeed - self.acc * self.deltaTime
        self.xzMoveSpeed = max(self.xzMoveSpeed, 0.0)
       
    def calcuteDelterPosition(self):
        accTime = abs(self.xzMoveSpeed) / self.acc
        accTime = min(accTime, self.deltaTime)
        #self.position = self.position +  self.xzMoveSpeed * self.deltaTime - 0.5 * self.acc * accTime * accTime

#根据路点的移动（移动方向和面朝向位置都是一样的）
class NormalMoveControler(MoveControllersBase):
    
    name = "NormalMoveControler"
    
    def __init__(self, owner, acc, minSpeed, maxSpeed):
        super(NormalMoveControler, self).__init__(owner)
        self.acc =  acc
        self.minSpeed = minSpeed
        self.maxSpeed = maxSpeed
        self.path = []  #路点信息
        self._destination = None
        self.nextId = 0
    
    def setSpeed(self, acc, minSpeed, maxSpeed):
        self.acc =  acc
        self.minSpeed = minSpeed
        self.maxSpeed = maxSpeed
        
    def setPath(self, _path, destination):
        self.path = _path
        self._destination = destination
        self.nextId = 0
        
    @property
    def path(self):
        return self.owner.aiMoviePath
    
    @path.setter
    def path(self, value):
        self.owner.aiMoviePath = value

    @property
    def nextId(self):
        return self.owner.aiMoviePathIndex

    @nextId.setter
    def nextId(self, value):
        self.owner.aiMoviePathIndex = value
        
    #重置信息
    def reset(self):
        MoveControllersBase.reset(self)
    
    def UpdateMoveSpeed(self):
        if self.xzMoveSpeed <= self.maxSpeed:
            self.xzMoveSpeed = min(self.xzMoveSpeed + self.acc, self.maxSpeed)
        else:
            self.xzMoveSpeed = max(self.xzMoveSpeed - self.acc, self.maxSpeed)

    def calcuteDelterPosition(self):
        if self.isDone():
            return
        accTime = abs(self.maxSpeed - self.xzMoveSpeed) / self.acc
        accTime = min(accTime, self.deltaTime)
        moveLen = self.xzMoveSpeed * self.deltaTime + 0.5 * self.acc * accTime * accTime
        
        nextPoint = self.path[self.nextId]
        _dis = nextPoint.distTo(self.position)
        _direction = nextPoint - self.position
        _direction.normalise()
        rotateAngle = math.atan2(_direction.x, _direction.z)
        self.direction = Math.Vector3(0, rotateAngle, 0)
        self.moveDirection = _direction

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
                rotateAngle = math.atan2(_direction.x, _direction.z)
                self.direction = Math.Vector3(0, rotateAngle, 0)
                self.moveDirection = _direction

            if moveLen < _dis:

                self.position = self.position + _direction * moveLen
            else:
                self.position = nextPoint
    
    #移动结束了
    def isDone(self):
        if self.nextId >= len(self.path):
            return True
        if self.owner.position.distTo(self._destination) < 0.5:
            return True
        return False

#随机移动的逻辑
class RandomWalkControler(NormalMoveControler):
    name = "RandomWalkControler"
    
    def __init__(self, owner, acc, minSpeed, maxSpeed, movePostion):
        super(RandomWalkControler, self).__init__(owner, acc, minSpeed, maxSpeed)
        self.movePosition = movePostion
        self.updatePath()

    def updatePath(self): 
        path = self.owner.navigatePathPoints(self.movePosition, 200, 0)
        self.setPath(path, path[-1])

   
#追逐目标的移动
class ChastEntityControler(NormalMoveControler):
    name = "ChastEntityControler"
    
    def __init__(self, owner, acc, minSpeed, maxSpeed, targetEntityId):
        super(ChastEntityControler, self).__init__(owner, acc, minSpeed, maxSpeed)
        self.targetEntityId = targetEntityId
        self.updatePath()
        
    def tick(self):
        super(ChastEntityControler, self).tick()
        if self.isDone():
            return
        self.updatePath()
           
    #移动结束了
    def isDone(self):
        spuerDone = super(ChastEntityControler, self).isDone()
        return spuerDone
    
    def updatePath(self): 
        target = KBEngine.entities.get(self.targetEntityId)
        path = self.owner.navigatePathPoints(target.position, 200, 0)
        self.setPath(path, path[-1])
    
#战斗时的移动控制
class FightMoveControler(NormalMoveControler):

    name = "FightMoveControler"
    
    def __init__(self, owner, acc, minSpeed, maxSpeed, entityId, movePostion):
        super(FightMoveControler, self).__init__(owner, acc, minSpeed, maxSpeed)
        self.targetEntityId = entityId
        self.movePosition = movePostion
        self.updatePath()
    
    def tick(self):
        super(FightMoveControler, self).tick()
        if self.isDone():
            return
        self.updatePath()
        
    def calcuteDelterPosition(self):
        super(FightMoveControler, self).calcuteDelterPosition()
        target = KBEngine.entities.get(self.targetEntityId)
        dir = target.position - self.owner.position
        rotateAngle = math.atan2(dir.x, dir.z)
        self.direction = Math.Vector3(0, rotateAngle, 0)  #始终朝向敌人
        
    #移动结束了
    def isDone(self):
        spuerDone = super(FightMoveControler, self).isDone()
        return spuerDone  
    
    def updatePath(self): 
        path = self.owner.navigatePathPoints(self.movePosition, 200, 0)
        self.setPath(path, path[-1])
    
#rootmotion移动
class RootMotionControler(MoveControllersBase):

    name = "RootMotionControler"
    
    def __init__(self, owner):
        super(RootMotionControler, self).__init__(owner)
        self.timeLineId = None
        self.aniClipName = None
       
    def setClip(self, clipName):
        self.aniClipName = clipName
        self.timeStamp = 0
        # self.curve = MotionCurve.MotionCurve(getRootMotion()[clipName])
        # self.reset()

    def reset(self):
        MoveControllersBase.reset(self)
        self.timeStamp = 0

    def UpdateMoveSpeed(self):
        self.xzMoveSpeed = 0.0

    def calcuteDelterPosition(self):
        pass
        # if self.isDone():
        #     return
        # _deltaV = self.curve.delterPosition(self.timeStamp, self.timeStamp + self.deltaTime)
        # deltaV = Math3D.rotationVector(self.direction, _deltaV)
        # self.timeStamp += self.deltaTime 
        # self.position = self.position + deltaV
        
    def isDone(self):
        return self.curve.isEnd(self.timeStamp)


#玩家非技能移动控制器
class PlayerMoveControler(MoveControllersBase):
    
    name = "PlayerMoveControler"
    
    def __init__(self, owner, acc, speed):
        super(PlayerMoveControler, self).__init__(owner)
        self.acc =  5.5 #停止时的加速度

    def UpdateMoveSpeed(self):
        self.xzMoveSpeed = self.xzMoveSpeed - self.acc * self.deltaTime
        self.xzMoveSpeed = max(self.xzMoveSpeed, 0.0)
       
    def calcuteDelterPosition(self):
        accTime = abs(self.xzMoveSpeed) / self.acc
        accTime = min(accTime, self.deltaTime)
        #self.position = self.position +  self.xzMoveSpeed * self.deltaTime - 0.5 * self.acc * accTime * accTime
