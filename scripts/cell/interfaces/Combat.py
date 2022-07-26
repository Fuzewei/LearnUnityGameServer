# -*- coding: utf-8 -*-
import KBEngine
import GlobalDefine
from KBEDebug import * 
from timeLine.TimeLineManager import TimeLineManager 
from timeLine.TimeLineBase import TimeLineBase 
from timeLine.TimeLineNodeBase import TimeLineNodeBase 
from interfaces.CombatPropertys import CombatPropertys
from SkillManager.SkillFactory import SkillFactory
from SkillManager.Skill import Skill
import moveControllers.BaseMoveControllers as Controllers

class Combat(CombatPropertys):
	"""
	关于战斗的一些功能
	"""
	def __init__(self):
		CombatPropertys.__init__(self)
		self.inBattle = False #在战斗中
		self.timeLineManager = TimeLineManager(self)
		self.skillFactory = SkillFactory()
		self.usingSkills = {}

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
		
	def addEnemy(self, entityID):
		"""
		defined.
		添加敌人
		"""
		if entityID in self.enemyLog:
			return

		DEBUG_MSG("%s::addEnemy: %i entity=%i" % \
						(self.getScriptName(), self.id, entityID))
		
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

	def serverRequestUseSkill(self, skillId):
		uuid = self.timeLineManager.getUUid()
		self.startP3ClientMove(self.getBestClient())
		self.doUseSkill(uuid, skillId)
		self.allClients.serverRequestUseSkill(uuid, skillId)

	def clientRequestUseSkill(self, exposed, uuid, skillId):
		self.doUseSkill(uuid, skillId)
		self.otherClients.serverRequestUseSkill(uuid, skillId)

	def doUseSkill(self, uuid, skillId):
		if self.usingSkills.get(skillId):
			assert(False)
		self.moveControllers = Controllers.RootMotionControler(self) #移动控制器
		skill = Skill(skillId, self)
		self.usingSkills[skillId] = skill
		skill.startTimeLine(skill.initTimeLineId, uuid)

	#打断技能
	def interruptSkill(self, skillId):
		skill = self.usingSkills.get(skillId)
		if skill:
			skill.interrupt()

	#技能结束的回调
	def onSkillFinish(self, skillId):
		del self.usingSkills[skillId]
		self.allClients.serverSkillFinish(skillId)
		self.moveControllers = Controllers.NormalIdleControler(self) #移动控制器
		self.stopP3ClientMove()

	def skillNodeCallServer(self, exposed, uuid, nodeId, args):
		print("skillNodeCallServer", exposed, self.id, uuid, nodeId, args)
		timeline = self.timeLineManager.getTimeLine(uuid)
		timeline.callFromClient(exposed, nodeId, args)
		#self.allClients.skillNodeCallClient(uuid, nodeId, args)


		
