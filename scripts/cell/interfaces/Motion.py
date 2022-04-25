# -*- coding: utf-8 -*-
import KBEngine
import math
import Math
import time
import random
from KBEDebug import *
from Const.MoveState import SERVER_MOVING_STAGE
from Const.MoveState import AI_RESULT 

class Motion:
	"""
	移动相关的封装
	"""
	def __init__(self):
		self.nextMoveTime = int(time.time() + random.randint(5, 15))
		self.movingType = SERVER_MOVING_STAGE.IDLE  #移动类型
		self.movingInfo = {} #移动信息
	
	def stopMotion(self):
		"""
		停止移动
		"""
		if self.isMoving:
			INFO_MSG("%i stop motion." % self.id)
			self.cancelController("Movement")
			self.isMoving = False
			self.movingType = SERVER_MOVING_STAGE.IDLE
			self.movingInfo = {}

	def _randomWalk(self, basePos, radius):
		"""
		随机移动entity
		"""

		if self.movingType == SERVER_MOVING_STAGE.RANDOM_MOVE:
			if self.position.distTo(self.movingInfo["destPos"]) < 0.5:
				self.stopMotion()
				return AI_RESULT.BT_SUCCESS
			return AI_RESULT.BT_RUNNING

		self.movingType = SERVER_MOVING_STAGE.RANDOM_MOVE
		_movingInfo = {}


		while True:
			# 移动半径距离在30米内
			if self.canNavigate():
				destPos = self.getRandomPoints(basePos, radius, 1, 0)
				if len(destPos) == 0:
					self.nextMoveTime = int(time.time() + random.randint(5, 15))
					return AI_RESULT.BT_SUCCESS
				
				destPos = destPos[0]
				_movingInfo["destPos"] = destPos
			else:
				rnd = random.random()
				a = 30.0 * rnd				# 移动半径距离在30米内
				b = 360.0 * rnd				# 随机一个角度
				x = a * math.cos( b ) 		# 半径 * 正余玄
				z = a * math.sin( b )
				
				destPos = (basePos.x + x, basePos.y, basePos.z + z)

			if self.position.distTo(destPos) < 2.0:
				continue
				
			self.gotoPosition(destPos)
			self.isMoving = True
			self.nextMoveTime = int(time.time() + random.randint(5, 15))
			self.movingInfo = _movingInfo
			break

		return AI_RESULT.BT_RUNNING

	def resetSpeed(self):
		walkSpeed = self.getDatas()["moveSpeed"]
		if walkSpeed != self.moveSpeed:
			self.moveSpeed = walkSpeed
				
	def backSpawnPos(self):
		"""
		virtual method.
		"""
		INFO_MSG("%s::backSpawnPos: %i, pos=%s, speed=%f." % \
			(self.getScriptName(), self.id, self.spawnPos, self.moveSpeed * 0.1))
		
		self.resetSpeed()
		self.gotoPosition(self.spawnPos)
	
	def gotoEntity(self, targetID, dist = 0.0):
		"""
		virtual method.
		移动到entity位置
		"""
		if self.isMoving:
			self.stopMotion()
		
		entity = KBEngine.entities.get(targetID)
		if entity is None:
			DEBUG_MSG("%s::gotoEntity: not found targetID=%i" % (targetID))
			return
			
		if entity.position.distTo(self.position) <= dist:
			return

		self.isMoving = True
		self.moveToEntity(targetID, self.moveSpeed * 0.1, dist, None, True, False)
		
	def gotoPosition(self, position, dist = 0.0):
		"""
		virtual method.
		移动到位置
		"""
		if self.isMoving:
			self.stopMotion()

		if self.position.distTo(position) <= 0.05:
			return

		self.isMoving = True
		speed = self.moveSpeed * 0.1
		
		if self.canNavigate():
			self.navigate(Math.Vector3(position), speed, dist, speed, 512.0, 1, 0, None)


		else:
			if dist > 0.0:
				destPos = Math.Vector3(position) - self.position
				destPos.normalise()
				destPos *= dist
				destPos = position - destPos
			else:
				destPos = Math.Vector3(position)
			
			self.moveToPoint(destPos, speed, 0, None, 1, False)

	def getStopPoint(self, yaw = None, rayLength = 100.0):
		"""
		"""
		if yaw is None:yaw = self.yaw
		yaw = (yaw / 2);
		vv = Math.Vector3(math.sin(yaw), 0, math.cos(yaw))
		vv.normalise()
		vv *= rayLength
		
		lastPos = self.position + vv;
		
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
