# -*- coding: utf-8 -*-
import time
from timeLine.TimeLineBase import TimeLineBase 

class SkillTimeLine(TimeLineBase):
    def __init__(self):
       TimeLineBase.__init__(self)

    @property
    def avatarOwner(self):
        return self.manager
    
    def onEnd(self):
        TimeLineBase.onEnd(self)

    def callFromClient(self, expose, nodeId, arg): #arg is TABLE
        node = self.nodesList[nodeId]
        assert(node)
        node.clientCall(expose, arg)

    def callAllClient(self, nodeId, arg): #arg is TABLE
        self.allClients.skillNodeCallClient(self.uuid, nodeId, arg)

    def callHostClient(self, nodeId, arg): #arg is TABLE
        self.client.skillNodeCallClient(self.uuid, nodeId, arg)

    def callOthersClient(self, nodeId, arg): #arg is TABLE
        self.otherClients.skillNodeCallClient(self.uuid, nodeId, arg)
