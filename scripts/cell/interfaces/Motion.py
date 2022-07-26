# -*- coding: utf-8 -*-
import KBEngine
import math
import Math
import time
import random
from KBEDebug import *
from Const.MoveState import SERVER_MOVING_STAGE
from Const.MoveState import AI_RESULT
from Const.MoveState import CLIENT_MOVE_CONST
import moveControllers.BaseMoveControllers as Controllers

class Motion:
	"""
	移动相关的封装,主要是服务端移动相关
	"""
	def __init__(self):
		self.baseTime = time.time()
		self.moveTickTimer = 0
		self.direction = Math.Vector3(0, 0, 1) #(全局移动方向)只给怪物用，后面再改
		self.moveDirection = Math.Vector3(0, 0, 1)  #（面朝方向全局）
		self.moveType = CLIENT_MOVE_CONST.Idel #客户端用的
		self.moveControllers = Controllers.NormalIdleControler(self) #移动控制器
  
		self.moveTickTimer = self.addTimerCallBack(0.1, 0.1, self.moveTickCallBack)
		self.hitFlyTimer = 0
  
	def moveTickCallBack(self, tid, *args):
		# if self.isClientMove():  #使用客户端移动
		# 	return
		self.moveControllers.tick()
		self.moveControllers.calcuteDelterPosition()  #返回相当于移动朝向的相对位移(vector3)
		self.moveControllers.UpdateMoveSpeed()
		self.allClients.confirmMoveTimeStamp(self.serverTime())


	def serverTime(self):
		self.confirmTime = time.time() - self.baseTime
		return self.confirmTime	

	def setRootMotionClip(self, clipId):
		self.moveControllers.setClip(clipId)
  
	#进入击飞状态，controlId表示击飞发起的客户端id，tid表示击飞状态定时器的id
	def switch2BeStrikefly(self, controlId, tid):
		if self.isUseingSkill():
			for skillID in list(self.usingSkills):
				self.interruptSkill(skillID)
		self.onBeStrikefly(controlId)
		self.moveType = CLIENT_MOVE_CONST.beStrikefly
		self.moveControllers = Controllers.RootMotionControler(self)
		self.allClients.confirmMoveTimeStamp(self.serverTime())
		if self.hitFlyTimer > 0:
			self.delTimerCallBack(self.hitFlyTimer)
		self.hitFlyTimer = tid

	#击飞状态结束
	def strikeflyDone(self, tid):
		assert(self.hitFlyTimer == tid)
		self.hitFlyTimer == 0
		self.moveType = CLIENT_MOVE_CONST.Idel #客户端用的
		self.moveControllers = Controllers.NormalIdleControler(self) #移动控制器
		self.allClients.confirmMoveTimeStamp(self.serverTime())
		self.onStrikeflyDone()

	def stopMotion(self):
		"""
		停止移动
		"""
		INFO_MSG("%i stop motion." % self.id)
		#self.cancelController("Movement")
		if self.moveType != CLIENT_MOVE_CONST.Idel: #客户端用的
			self.moveType = CLIENT_MOVE_CONST.Idel #客户端用的
			self.moveControllers = Controllers.NormalIdleControler(self) #移动控制器
			self.allClients.confirmMoveTimeStamp(self.serverTime())

	def _aiFightMove(self, moveId, tarEntityId, movePostion):
		self.moveType = CLIENT_MOVE_CONST.Walk #客户端用的
		self.moveControllers = Controllers.FightMoveControler(self, 3.76, 0, 2.21, tarEntityId, movePostion) #移动控制器
		self.allClients.confirmMoveTimeStamp(self.serverTime())

	def _randomWalk(self, basePos, radius):
		"""
		随机移动entity
		"""
		#当前已经在随机移动了
		if self.moveControllers.name == "RandomWalkControler":
			if self.moveControllers.isDone():
				return AI_RESULT.BT_SUCCESS
			return AI_RESULT.BT_RUNNING

		self.moveType = CLIENT_MOVE_CONST.Walk #客户端用的
		self.allClients.confirmMoveTimeStamp(self.serverTime())
		
		destPos = self.getRandomPoints(basePos, radius, 1, 0)
		if len(destPos) == 0:
			return AI_RESULT.BT_SUCCESS
		destPos = destPos[0]
		self.moveControllers = Controllers.RandomWalkControler(self, 3.76, 0, 2.21, destPos)

		self.isMoving = True
		return AI_RESULT.BT_RUNNING
	
	def _gotoEntity(self, targetID, dist = 1):
		"""
		移动到entity位置
		"""
		INFO_MSG("_gotoEntity = %s. %s" % (targetID, type(targetID)))

		if self.moveControllers.name == "ChastEntityControler" and self.moveControllers.targetEntityId == targetID:
			if self.moveControllers.isDone():
				return AI_RESULT.BT_SUCCESS
			return AI_RESULT.BT_RUNNING
		self.moveType = CLIENT_MOVE_CONST.Run #客户端用的(跑)
		self.allClients.confirmMoveTimeStamp(self.serverTime())
		self.moveControllers = Controllers.ChastEntityControler(self, 10.8, 0, 5.05, targetID)
		self.isMoving = True
		return AI_RESULT.BT_RUNNING

	def getStopPoint(self, yaw = None, rayLength = 100.0):
		"""
		"""
		if yaw is None:yaw = self.yaw
		yaw = (yaw / 2)
		vv = Math.Vector3(math.sin(yaw), 0, math.cos(yaw))
		vv.normalise()
		vv *= rayLength
		
		lastPos = self.position + vv
		
		pos = KBEngine.raycast(self.spaceID, self.layer, self.position, vv)
		if pos == None:
			pos = lastPos
		return pos

	#--------------------------------------------------------------------------------------------
	#                              Callbacks
	#--------------------------------------------------------------------------------------------
	def onMove(self, controllerId, userarg):
		"""
		KBEngine method.
		使用引擎的任何移动相关接口， 在entity一次移动完成时均会调用此接口
		"""
		#DEBUG_MSG("%s::onMove: %i controllerId =%i, userarg=%s" % \
		#				(self.getScriptName(), self.id, controllerId, userarg))
		self.isMoving = True
		
	def onMoveFailure(self, controllerId, userarg):
		"""
		KBEngine method.
		使用引擎的任何移动相关接口， 在entity一次移动完成时均会调用此接口
		"""
		DEBUG_MSG("%s::onMoveFailure: %i controllerId =%i, userarg=%s" % \
						(self.getScriptName(), self.id, controllerId, userarg))
		
		self.isMoving = False
		self.movingType = SERVER_MOVING_STAGE.IDLE
		
	def onMoveOver(self, controllerId, userarg):
		"""
		KBEngine method.
		使用引擎的任何移动相关接口， 在entity移动结束时均会调用此接口
		"""	
		self.isMoving = False
		self.movingType = SERVER_MOVING_STAGE.IDLE

