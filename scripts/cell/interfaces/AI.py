# -*- coding: utf-8 -*-
import KBEngine
import SCDefine
import Math
import traceback
import random
import GlobalDefine
from KBEDebug import * 
from Const.MoveState import AI_RESULT 
from Const.MoveState import SERVER_MOVING_STAGE
from Const.MoveState import CLIENT_MOVE_CONST
from AICls.AiSkillUseInfoDecision import AiSkillUseDecision
from AICls.AiMoveDecision import AiMoveDecision

__TERRITORY_AREA__ = 60

class AI:
	def __init__(self):
		self.aiSkillUseBrain = {}
		self.aiMoveDecision = AiMoveDecision(self.id)
		self.aiMovingType = SERVER_MOVING_STAGE.IDLE #设置ai的移动类型
		self.addTimerCallBack(0.1, 0, self.initAi)
  
	def initAi(self, tid, *args):
		"""
		初始化ai
		"""
		self.addTerritory()
		self.initAiController("EasyMonster")
		self.heartBeatTimerID = self.addTimerCallBack(random.randint(0, 1), 1, self.onHeartTick)

	def onHeartTick(self, tid, *args):
		"""
		entity的心跳
		"""
		self.updateAiController() #c++行为树tick

	def checkInTerritory(self):
		"""
		virtual method.
		检查自己是否在可活动领地中
		"""
		ret = self.position.distTo(self.spawnPos) <= __TERRITORY_AREA__
		if not ret:
			INFO_MSG("%s::checkInTerritory: %i is False." % (self.getScriptName(), self.id))
			
		return ret

	def addTerritory(self):
		"""
		添加领地
		进入领地范围的某些entity将视为敌人
		"""
		assert self.territoryControllerID == 0
		trange = __TERRITORY_AREA__ / 2.0
		self.territoryControllerID = self.addProximity(trange, 0, 0)
		
		if self.territoryControllerID <= 0:
			ERROR_MSG("%s::addTerritory: %i, range=%i, is error!" % (self.getScriptName(), self.id, trange))
		else:
			INFO_MSG("%s::addTerritory: %i range=%i, id=%i." % (self.getScriptName(), self.id, trange, self.territoryControllerID))
			
	def delTerritory(self):
		"""
		删除领地(暂无)
		"""
		if self.territoryControllerID > 0:
			self.cancelController(self.territoryControllerID)
			self.territoryControllerID = 0
			INFO_MSG("%s::delTerritory: %i" % (self.getScriptName(), self.id))


	def disable(self):
		"""
		禁止这个entity做任何行为
		"""
		self.delTimer(self.heartBeatTimerID)
		self.heartBeatTimerID = 0
	
	def setTarget(self, entityID):
		"""
		设置目标
		"""
		self.targetID = entityID
		self.onTargetChanged()
	
	#--------------------------------------------------------------------------------------------
	#                              Callbacks
	#--------------------------------------------------------------------------------------------

	#行为树调用函数0=BT_INVALID,1=BT_SUCCESS,2=BT_FAILURE,3=BT_RUNNING
	def onBhCallFunc(self, funcName, arg):
		INFO_MSG("onBhCallFunc = %s. " % (funcName, ))
		func = getattr(self, funcName)
		result = AI_RESULT.BT_FAILURE
		if callable(func):
			try:
				result = func(arg)
			except Exception as e:
				print("error", e)
				traceback.print_exc()
				
		return result
		

	#行为树叶子节点调用函数begin(先这么写)

	def randomWalk(self, radius):
		"""
		entity在周边随机走动
		"""
		INFO_MSG("randomWalk = %s." % (radius, ))
		if self.territoryControllerID <= 0:
			self.addTerritory()
		result = self._randomWalk(self.position, radius)
		if result == AI_RESULT.BT_SUCCESS:
			self.stopMotion()
			self.aiMovingType = SERVER_MOVING_STAGE.IDLE#ai的移动类型
			self.allClients.stopMotion()
		elif result == AI_RESULT.BT_RUNNING:
			self.aiMovingType = SERVER_MOVING_STAGE.RANDOM_MOVE#服务端的移动类型
			self.allClients.randomWalk()

		return result

	#跑步移动到指定id的entitiy
	def chaseTarget(self, entityId):
		"""
		entity移动到entity
		"""
		INFO_MSG("moveToEntity = %s." % (entityId, ))

		if self.territoryControllerID <= 0:
			self.addTerritory()
		result = self._gotoEntity(entityId, 0.5)
		if result == AI_RESULT.BT_SUCCESS:
			self.stopMotion()
			self.aiMovingType = SERVER_MOVING_STAGE.IDLE#ai的移动类型
			self.allClients.stopMotion()
		elif result == AI_RESULT.BT_RUNNING:
			self.aiMovingType = SERVER_MOVING_STAGE.CHAST_RUN
			self.allClients.chaseTarget(entityId)
		return result

	#原地静止
	def idle(self, *args):
		"""
		entity原地静止
		"""
		INFO_MSG("idle = ")
		self.stopMotion()	
		self.aiMovingType = SERVER_MOVING_STAGE.IDLE#ai的移动类型
		self.allClients.stopMotion()

		return AI_RESULT.BT_RUNNING

	#能否使用指定技能id
	def canSkillAttack(self, skillId):
		INFO_MSG("canSkillAttack = %s" % (skillId, ))
		enemy = KBEngine.entities.get(self.targetID)
		if not enemy :
			return AI_RESULT.BT_FAILURE

		if self.isBeStrikefly() or self.isUseingSkill(): #被击退或正在使用技能
			return AI_RESULT.BT_FAILURE

		skillUseInfo = self.aiSkillUseBrain.setdefault(skillId, AiSkillUseDecision(skillId, self.id))
		if not skillUseInfo.canUse(self.targetID):
			return AI_RESULT.BT_FAILURE

		return AI_RESULT.BT_SUCCESS

	def useSkill(self, useSkillInfo):
		entityId = useSkillInfo[0]
		skillId = useSkillInfo[1]
		INFO_MSG("entityId %s useSkill = %s." % (entityId, skillId))
		self.aiMovingType = SERVER_MOVING_STAGE.USING_SKILL
		self.moveType = CLIENT_MOVE_CONST.Skill
		self.allClients.confirmMoveTimeStamp(self.serverTime())
		self.serverRequestUseSkill(skillId)
		self.allClients.useSkill(entityId, skillId)
		self.aiSkillUseBrain.setdefault(skillId, AiSkillUseDecision(skillId, self.id)).onUseSkill(entityId)
		return AI_RESULT.BT_SUCCESS

	#返回敌人的信息，行为树使用
	def getEnemyInfo(self, *none):
		enemy = KBEngine.entities.get(self.targetID)
		return (self.targetID, self.position.distTo(enemy.position)) 

	#刷新攻击目标
	def findEnemys(self, *args):
		if len(self.enemyLog) > 1:
			pass
		return AI_RESULT.BT_SUCCESS

	#行为树设置进入战斗状态
	def aiSetInBattle(self, _inbattle):
		if self.inBattle != _inbattle:
			self.inBattle = _inbattle
			self.allClients.confirmMoveTimeStamp(self.serverTime())
			if	self.inBattle:
				pass
				#self.startP3ClientMove(self.getBestClient())
			else:
				pass
				#self.stopP3ClientMove()
		return AI_RESULT.BT_SUCCESS 

	#战斗中移动走位，默认朝向敌人,moveId(表示以何种方式移动到目标点)，movePostion是位置
	def fightMove(self, fightMoveInfo):
		"""
		entity在走动
		"""
		moveId = fightMoveInfo[0]
		movePostion = fightMoveInfo[1]
		INFO_MSG("fightMove = %s." % (movePostion, ))

		self._aiFightMove(moveId, self.targetID, movePostion)

		self.aiMovieToPoint = Math.Vector3(movePostion)
		self.aiMovingType = SERVER_MOVING_STAGE.FIGHT_MOVE#服务端的移动类型
		self.allClients.fightMove(moveId, self.aiMovieToPoint)
		return AI_RESULT.BT_SUCCESS 


	#ai请求计算战斗中的移动位置（moveId为移动类型，帮助获取移动位置）
	def getFightMoveTarget(self, moveId):
		"""
		计算entity的移动目标点
		"""
		INFO_MSG("getFightMoveTarget = %s." % (moveId, ))
		return self.aiMoveDecision.getMovePoint(moveId)


	#行为树叶子节点调用函数end
	def onBeStrikefly(self, strikeId):
		"""
		virtual method.
		自己被击飞
		"""
		self.aiMovingType = SERVER_MOVING_STAGE.BE_ATTACK


	def onStrikeflyDone(self):
		"""
		virtual method.
		被击飞结束
		"""
		self.allClients.stopMotion()
		self.aiMovingType = SERVER_MOVING_STAGE.IDLE#ai的移动类型
		self.allClients.stopMotion()

		
	def onTargetChanged(self):
		"""
		virtual method.
		目标改变
		"""
		pass
		
	def onWitnessed(self, isWitnessed):
		"""
		KBEngine method.
		此实体是否被观察者(player)观察到, 此接口主要是提供给服务器做一些性能方面的优化工作，
		在通常情况下，一些entity不被任何客户端所观察到的时候， 他们不需要做任何工作， 利用此接口
		可以在适当的时候激活或者停止这个entity的任意行为。
		@param isWitnessed	: 为false时， entity脱离了任何观察者的观察
		"""
		INFO_MSG("%s::onWitnessed: %i isWitnessed=%i." % (self.getScriptName(), self.id, isWitnessed))
		

	def onStateChanged_(self, oldstate, newstate):
		"""
		virtual method.
		entity状态改变了
		"""
		pass
	
	def onEnterTrap(self, entityEntering, range_xz, range_y, controllerID, userarg):
		"""
		KBEngine method.
		有entity进入trap
		"""
		DEBUG_MSG("::onEnterTrap:%i and %i and %s" % (controllerID, self.territoryControllerID, entityEntering.getScriptName()))
		# if controllerID != self.territoryControllerID:
		# 	return
		DEBUG_MSG("::onEnterTrap:111")
		if entityEntering.isDestroyed or entityEntering.getScriptName() != "Avatar" or entityEntering.isDead():
			return
		
			
		DEBUG_MSG("%s::onEnterTrap: %i entityEntering=(%s)%i, range_xz=%s, range_y=%s, controllerID=%i, userarg=%i" % \
						(self.getScriptName(), self.id, entityEntering.getScriptName(), entityEntering.id, \
						range_xz, range_y, controllerID, userarg))
		
		self.addEnemy(entityEntering.id)

	def onLeaveTrap(self, entityLeaving, range_xz, range_y, controllerID, userarg):
		"""
		KBEngine method.
		有entity离开trap
		"""
		if controllerID != self.territoryControllerID:
			return
		
		if entityLeaving.isDestroyed or entityLeaving.getScriptName() != "Avatar" or entityLeaving.isDead():
			return
			
		INFO_MSG("%s::onLeaveTrap: %i entityLeaving=(%s)%i." % (self.getScriptName(), self.id, \
				entityLeaving.getScriptName(), entityLeaving.id))
		self.removeEnemy(entityLeaving.id)

	def onAddEnemy(self, entityID):
		"""
		virtual method.
		有敌人进入列表
		"""
		if not self.isState(GlobalDefine.ENTITY_STATE_FIGHT):
			self.changeState(GlobalDefine.ENTITY_STATE_FIGHT)
		
		if self.targetID == 0:
			self.setTarget(entityID)
			
	def onRemoveEnemy(self, entityID):
		"""
		virtual method.
		删除敌人
		"""
		if self.targetID == entityID:
			self.onLoseTarget()

	def onLoseTarget(self):
		"""
		敌人丢失
		"""
		INFO_MSG("%s::onLoseTarget: %i target=%i, enemyLogSize=%i." % (self.getScriptName(), self.id, \
				self.targetID, len(self.enemyLog)))
				
		self.targetID = 0
		
		if len(self.enemyLog) > 0:
			self.targetID = self.enemyLog[0]


	def onEnemyEmpty(self):
		"""
		virtual method.
		敌人列表空了
		"""
		INFO_MSG("%s::onEnemyEmpty: %i" % (self.getScriptName(), self.id))

		if not self.isState(GlobalDefine.ENTITY_STATE_FREE):
			self.changeState(GlobalDefine.ENTITY_STATE_FREE)

