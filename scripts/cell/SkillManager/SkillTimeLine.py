# -*- coding: utf-8 -*-
import time
from timeLine.TimeLineBase import TimeLineBase 

class SkillTimeLine(TimeLineBase):
    def __init__(self):
       TimeLineBase.__init__(self)
       self.skill = None

    def setBelongSkil(self, _skill):
        self.skill = _skill

    @property
    def avatarOwner(self):
        return self.manager.avatar
    
    def onEnd(self):
        self.skill.onTimeLineFinish(self.uuid)
        self.skill = None
        TimeLineBase.onEnd(self)

    def callFromClient(self, expose, nodeId, arg): #arg is TABLE
        node = self.nodesList[nodeId]
        assert(node)
        node.clientCall(expose, arg)

    def callAllClient(self, nodeId, arg): #arg is TABLE
        self.avatarOwner.allClients.skillNodeCallClient(self.uuid, nodeId, arg)

    def callHostClient(self, nodeId, arg): #arg is TABLE
        self.avatarOwner.client.skillNodeCallClient(self.uuid, nodeId, arg)

    def callOthersClient(self, nodeId, arg): #arg is TABLE
        self.avatarOwner.otherClients.skillNodeCallClient(self.uuid, nodeId, arg)
