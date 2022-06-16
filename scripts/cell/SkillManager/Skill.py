# -*- coding: utf-8 -*-
from KBEDebug import * 
import time
from timeLine.TimeLineBase import TimeLineBase 

class Skill:

    def __init__(self, _id, _avatar):
       self.timeLineUUIDs = {}
       self.skillId = _id
       self.initTimeLineId = _id
       self.avatar = _avatar
       self.beginTime = time.time()

    def startTimeLine(self, timeLineId, uuid):
        timeline = self.avatar.skillFactory.getSkillBeginTimeLine(timeLineId)
        timeline.setBelongSkil(self)
        self.avatar.timeLineManager.addTimeLine(uuid, timeline)
        self.timeLineUUIDs[uuid] = timeline

    #skill管理的timeline运行结束，timeline结束时调用
    def onTimeLineFinish(self, uuid):
        timeline = self.timeLineUUIDs.get(uuid)
        assert(timeline)
        del self.timeLineUUIDs[uuid]
        if len(self.timeLineUUIDs) == 0:
            self.onFininsh()

    #技能被打断调用
    def interrupt(self):
        for uuid in list(self.timeLineUUIDs):
            self.avatar.timeLineManager.delTimeLine(uuid)
        

    def onFininsh(self):
        self.avatar.onSkillFinish(self.skillId)
        self.avatar = None
        INFO_MSG("onSkillFinish = %s. delterTime = %s" % (self.skillId, time.time() - self.beginTime))

    



