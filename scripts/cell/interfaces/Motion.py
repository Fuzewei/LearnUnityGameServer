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
	移动相关的封装
	"""
	def __init__(self):
		self.baseTime = time.time()
		self.moveTickTimer = 0
		self.direction = Math.Vector3(0, 0, 1) #(全局移动方向)只给怪物用，后面再改
		self.moveDirection = Math.Vector3(0, 0, 1)  #（面朝方向全局）
		self.switchMoveStage(SERVER_MOVING_STAGE.IDLE)

	def serverTime():
		return time.time() - self.baseTime
	

	def switchMoveStage(self, newStage):
		if newStage == SERVER_MOVING_STAGE.IDLE:
			self.aiMovingType = SERVER_MOVING_STAGE.IDLE#服务端的移动类型
			self.moveType = CLIENT_MOVE_CONST.Idel #客户端用的
			self.movingInfo = {}#移动信息
			self.moveControllers = Controllers.NormalIdleControler(self) #移动控制器
		elif newStage == SERVER_MOVING_STAGE.RANDOM_MOVE:
			self.aiMovingType = SERVER_MOVING_STAGE.RANDOM_MOVE
			self.moveType = CLIENT_MOVE_CONST.Walk #客户端用的
			self.movingInfo = {}
			self.moveControllers = Controllers.NormalWalkControler(self)
		elif newStage == SERVER_MOVING_STAGE.ROOTMOTION:
			self.aiMovingType = SERVER_MOVING_STAGE.ROOTMOTION
			self.moveType = CLIENT_MOVE_CONST.Walk #客户端用的
			self.movingInfo = {}
			self.moveControllers = Controllers.RootMotionControler(self)
		elif newStage == SERVER_MOVING_STAGE.CHAST_RUN:
			self.aiMovingType = SERVER_MOVING_STAGE.CHAST_RUN
			self.moveType = CLIENT_MOVE_CONST.Run #客户端用的
			self.movingInfo = {}
			self.moveControllers = Controllers.NormalRunControler(self)
		elif newStage == SERVER_MOVING_STAGE.USING_SKILL:
			self.aiMovingType = SERVER_MOVING_STAGE.USING_SKILL
			self.moveType = CLIENT_MOVE_CONST.Idel #客户端用的
			self.movingInfo = {}
			self.moveControllers = Controllers.NormalIdleControler(self)
		self.moveControllers.reset()
	
	def stopMotion(self):
		"""
		停止移动
		"""
		if self.isMoving:
			INFO_MSG("%i stop motion." % self.id)
			#self.cancelController("Movement")
			self.isMoving = False
			self.switchMoveStage(SERVER_MOVING_STAGE.IDLE)
			self.allClients.confirmMoveTimeStamp(time.time() - self.baseTime)
			self.allClients.stopMotion()

	def _randomWalk(self, basePos, radius):
		"""
		随机移动entity
		"""
		#当前已经在随机移动了

		if self.aiMovingType == SERVER_MOVING_STAGE.RANDOM_MOVE:
			if self.position.distTo(self.movingInfo["destPos"]) < 0.5:
				self.stopMotion()
				return AI_RESULT.BT_SUCCESS
			return AI_RESULT.BT_RUNNING

		self.switchMoveStage(SERVER_MOVING_STAGE.RANDOM_MOVE)	

		if self.canNavigate():
			destPos = self.getRandomPoints(basePos, radius, 1, 0)
			if len(destPos) == 0:
				return AI_RESULT.BT_SUCCESS
			destPos = destPos[0]
			self.movingInfo["destPos"] = destPos
			self.movingInfo["path"] = self.navigatePathPoints(destPos, 100, 0)
			self.movingInfo["nextId"] = 0
		else:
			assert(False)
		
		self.startTick()
		self.isMoving = True
		self.allClients.confirmMoveTimeStamp(time.time() - self.baseTime)
		self.allClients.randomWalk(self.movingInfo["path"])

		return AI_RESULT.BT_RUNNING

	def _rootMotionMove(self, clipName = "GreatSword_Attack01"):
		"""
		rootMotion移动
		"""
		if self.aiMovingType == SERVER_MOVING_STAGE.ROOTMOTION:
			if self.moveControllers.isEnd():
				self.stopMotion()
				return AI_RESULT.BT_SUCCESS
			return AI_RESULT.BT_RUNNING

		self.switchMoveStage(SERVER_MOVING_STAGE.ROOTMOTION)
		self.moveControllers.setClip(clipName)
		self.startTick()
		self.isMoving = True
		return AI_RESULT.BT_RUNNING
	
	def _gotoEntity(self, targetID, dist = 1):
		"""
		移动到entity位置
		"""
		INFO_MSG("_gotoEntity = %s. %s" % (targetID, type(targetID)))

		target = KBEngine.entities.get(targetID)
		if self.position.distTo(target.position) < dist:
			self.stopMotion()
			return AI_RESULT.BT_SUCCESS

		if self.canNavigate():
			self.movingInfo["destPos"] = target.position
			self.movingInfo["path"] = self.navigatePathPoints(target.position, 200, 0)
			self.movingInfo["nextId"] = 0
		else:
			assert(False)

		if self.aiMovingType == SERVER_MOVING_STAGE.CHAST_RUN:
			return AI_RESULT.BT_RUNNING

		self.switchMoveStage(SERVER_MOVING_STAGE.CHAST_RUN)
			
		self.startTick()
		self.isMoving = True
		self.allClients.confirmMoveTimeStamp(time.time() - self.baseTime)
		self.allClients.chaseTarget(targetID)
		return AI_RESULT.BT_RUNNING

	
	def startTick(self):
		"""
		virtual method.
		移动tick
		"""
		
		if self.moveTickTimer == 0:
			self.moveTickTimer = self.addTimerCallBack(0, 0.1, self.moveTickCallBack)



	def moveTickCallBack(self, tid, *args):
		self.moveControllers.tick()
		self.moveControllers.calcuteDelterPosition()  #返回相当于移动朝向的相对位移(vector3)
		self.moveControllers.UpdateMoveSpeed()
		self.allClients.confirmMoveTimeStamp(time.time() - self.baseTime)
	
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
		self.movingInfo = {}
		
	def onMoveOver(self, controllerId, userarg):
		"""
		KBEngine method.
		使用引擎的任何移动相关接口， 在entity移动结束时均会调用此接口
		"""	
		self.isMoving = False
		self.movingType = SERVER_MOVING_STAGE.IDLE
		self.movingInfo = {}
