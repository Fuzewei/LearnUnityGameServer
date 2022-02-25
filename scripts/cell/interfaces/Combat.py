# -*- coding: utf-8 -*-
import KBEngine
import GlobalDefine
from KBEDebug import * 
from timeLine.TimeLineManager import TimeLineManager 
from timeLine.TimeLineBase import TimeLineBase 
from timeLine.TimeLineNodeBase import TimeLineNodeBase 
from interfaces.CombatPropertys import CombatPropertys

class Combat(CombatPropertys):
	"""
	关于战斗的一些功能
	"""
	def __init__(self):
		CombatPropertys.__init__(self)
		self.inBattle = False
		self.timeLineManager = TimeLineManager(self)

	def canUpgrade(self):
		"""
		virtual method.
		"""
		return True
		
	def upgrade(self):
		"""
		for real
		"""
		if self.canUpgrade():
			self.addLevel(1)
			
	def addLevel(self, lv):
		"""
		for real
		"""
		self.level += lv
		self.onLevelChanged(lv)
		
	def isDead(self):
		"""
		"""
		return self.state == GlobalDefine.ENTITY_STATE_DEAD
		
	def die(self, killerID):
		"""
		"""
		if self.isDestroyed or self.isDead():
			return
		
		if killerID == self.id:
			killerID = 0
			
		INFO_MSG("%s::die: %i i die. killerID:%i." % (self.getScriptName(), self.id, killerID))
		killer = KBEngine.entities.get(killerID)
		if killer:
			killer.onKiller(self.id)
			
		self.onBeforeDie(killerID)
		self.onDie(killerID)
		self.changeState(GlobalDefine.ENTITY_STATE_DEAD)
		self.onAfterDie(killerID)
	
	def canDie(self, attackerID, skillID, damageType, damage):
		"""
		virtual method.
		是否可死亡
		"""
		return True
		
	def recvDamage(self, attackerID, skillID, damageType, damage):
		"""
		defined.
		"""
		if self.isDestroyed or self.isDead():
			return
		
		self.addEnemy(attackerID, damage)

		DEBUG_MSG("%s::recvDamage: %i attackerID=%i, skillID=%i, damageType=%i, damage=%i" % \
			(self.getScriptName(), self.id, attackerID, skillID, damageType, damage))
			
		if self.HP <= damage:
			if self.canDie(attackerID, skillID, damageType, damage):
				self.die(attackerID)
		else:
			self.setHP(self.HP - damage)
		
		self.allClients.recvDamage(attackerID, skillID, damageType, damage)
		
	def addEnemy(self, entityID, enmity):
		"""
		defined.
		添加敌人
		"""
		if entityID in self.enemyLog:
			return

		DEBUG_MSG("%s::addEnemy: %i entity=%i, enmity=%i" % \
						(self.getScriptName(), self.id, entityID, enmity))
		
		self.enemyLog.append(entityID)
		self.onAddEnemy(entityID)
		
	def removeEnemy(self, entityID):
		"""
		defined.
		删除敌人
		"""
		DEBUG_MSG("%s::removeEnemy: %i entity=%i" % \
						(self.getScriptName(), self.id, entityID))
		
		self.enemyLog.remove(entityID)
		self.onRemoveEnemy(entityID)
	
		if len(self.enemyLog) == 0:
			self.onEnemyEmpty()

	def checkInTerritory(self):
		"""
		virtual method.
		检查自己是否在可活动领地中
		"""
		return True

	def checkEnemyDist(self, entity):
		"""
		virtual method.
		检查敌人距离
		"""
		dist = entity.position.distTo(self.position)
		if dist > 30.0:
			INFO_MSG("%s::checkEnemyDist: %i id=%i, dist=%f." % (self.getScriptName(), self.id, entity.id, dist))
			return False
		
		return True
		
	def checkEnemys(self):
		"""
		检查敌人列表
		"""
		for idx in range(len(self.enemyLog) - 1, -1, -1):
			entity = KBEngine.entities.get(self.enemyLog[idx])
			if entity is None or entity.isDestroyed or entity.isDead() or \
				not self.checkInTerritory() or not self.checkEnemyDist(entity):
				self.removeEnemy(self.enemyLog[idx])

	#--------------------------------------------------------------------------------------------
	#                              Callbacks
	#--------------------------------------------------------------------------------------------
	def onLevelChanged(self, addlv):
		"""
		virtual method.
		"""
		pass
		
	def onDie(self, killerID):
		"""
		virtual method.
		"""
		self.setHP(0)
		self.setMP(0)

	def onBeforeDie(self, killerID):
		"""
		virtual method.
		"""
		pass

	def onAfterDie(self, killerID):
		"""
		virtual method.
		"""
		pass
	
	def onKiller(self, entityID):
		"""
		defined.
		我击杀了entity
		"""
		pass
		
	def onDestroy(self):
		"""
		entity销毁
		"""
		pass
		
	def onAddEnemy(self, entityID):
		"""
		virtual method.
		有敌人进入列表
		"""
		pass

	def onRemoveEnemy(self, entityID):
		"""
		virtual method.
		删除敌人
		"""
		pass

	def onEnemyEmpty(self):
		"""
		virtual method.
		敌人列表空了
		"""
		pass



	#--------------------------------------------------------------------------------------------
	#                              技能系统代码，后期在整理fzw
	#--------------------------------------------------------------------------------------------

	def clientRequestUseSkill(self, exposed, uuid, skillId):
		timeline = self.getTimeLineById(skillId)
		self.timeLineManager.addTimeLine(uuid, timeline)
		self.otherClients.serverRequestUseSkill(uuid, skillId)

	def skillNodeCallServer(self, exposed, uuid, nodeId, args):
		print("skillNodeCallServer", uuid, nodeId, args, type(args))
		entityId = args[0]
		entity = KBEngine.entities.get(entityId)
		entity.setAvatarMoveState(6) #移动状态变为服务端驱动
		self.allClients.skillNodeCallClient(uuid, nodeId, args)
	

	def getTimeLineById(self, skillId):
		timeline = TimeLineBase()
		node1 = TimeLineNodeBase(1)
		timeline.addNode(node1)
		node2 = TimeLineNodeBase(1.5)
		timeline.addNode(node2)
		node4 = TimeLineNodeBase(5.5)
		timeline.addNode(node4)
		node3 = TimeLineNodeBase(20.5)
		timeline.addNode(node3) 
		return timeline
