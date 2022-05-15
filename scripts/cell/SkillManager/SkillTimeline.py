# -*- coding: utf-8 -*-
import time
from timeLine.TimeLineBase import TimeLineBase 

class SkillTimeLine(TimeLineBase):
    def __init__(self):
       TimeLineBase.__init__(self)
    

    def callFromClient(self, nodeId, arg): #arg is TABLE
        node = self.nodesList[nodeId]
        assert(node)
        node.clientCall(arg)

    def callAllClient(self, nodeId, arg): #arg is TABLE
        
        pass

    def callHostClient(self, nodeId, arg): #arg is TABLE
        
        pass

    def callOthersClient(self, nodeId, arg): #arg is TABLE
        
        pass
