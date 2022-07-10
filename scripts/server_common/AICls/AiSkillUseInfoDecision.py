# -*- coding: utf-8 -*-
import time
import random
import KBEngine

class AiSkillUseBase():

    def __init__(self, skillId, srcEntityId):
        self.skillId = skillId
        self.srcEntityId = srcEntityId
        self.tarEntityId = None #技能攻击的目标
        self.useTime = 0 #技能释放时间

     #返回是否能使用本技能
    def canUse(self, _tarEntityId):
        return True
    
    #当被使用后调用，表示使用的技能的对象
    def onUseSkill(self, _tarEntityId):
        self.tarEntityId = _tarEntityId
        self.useTime = time.time()
    
    #返回指定技能id的使用信息
    @property
    def aiSkillUseBrain(self):
        if self.avatar:
            return self.avatar.aiSkillUseBrain
        
    @property
    def avatar(self):
        return KBEngine.entities.get(self.srcEntityId)

class SkillCommonAttack(AiSkillUseBase):

    def __init__(self, skillId, srcEntityId):
        super(SkillCommonAttack, self).__init__(skillId, srcEntityId)
        
    #ai使用技能的概率
    def getUseProbability(self):
        otherSkillId = None
        recentSkillTime = 0
        for skillId, skill in self.aiSkillUseBrain.items():
            if skill.useTime > recentSkillTime and skill.skillId != self.skillId:
                recentSkillTime = skill.useTime
                otherSkillId = skillId
        if not otherSkillId :
            return 0.7
        
        
        if time.time() - recentSkillTime < 1.2:
            return 0.0
        if 1.2 <= time.time() - recentSkillTime < 2:
            return 0.3
        if 2 <= time.time() - recentSkillTime < 3:
            return 0.8
        return 0.9
        
    def canUse(self, _tarEntityId):
        if time.time() - self.useTime < 3.5: #技能cd
            return False
        enemy = KBEngine.entities.get(_tarEntityId)
        distance = self.avatar.position.distTo(enemy.position)
        if distance > 4:  #攻击不到
            return False

        if  random.random() < self.getUseProbability():
            return True
        else:
            return False
      
    def onUseSkill(self, _tarEntityId):
        super(SkillCommonAttack, self).onUseSkill(_tarEntityId)



#ai能否使用某技能
class AiSkillUseDecision():
    SkillUseCls = {
        1 : SkillCommonAttack,
        2 : AiSkillUseBase,
        3 : AiSkillUseBase
    }

    def __new__(cls, skillId, srcEntityId):
        useCls = AiSkillUseDecision.SkillUseCls.get(skillId)
        if not useCls:
            assert(False)
        return useCls(skillId, srcEntityId)