# -*- coding: utf-8 -*-
import time
import KBEngine

class TimeLineManager():
    def __init__(self, owner):
        self.owner = owner
        self.nodeUUid = 0
        self.timeLines = {}
        self.nextDelterTime = float('inf')
        self.updateTimerId = 0

    
    def getUUid(self):
        a = self.nodeUUid
        self.nodeUUid += 1
        return a 

    def addTimeLine(self, uuid, timeline):
        timeline.setManager(self)
        timeline.start()
        self.timeLines[uuid] = timeline
        if timeline.getNextDelterTime() < self.nextDelterTime:
            if self.updateTimerId > 0 :
                self.owner.delTimerCallBack(self.updateTimerId)
            self.nextDelterTime = timeline.getNextDelterTime()
            self.updateTimerId = self.owner.addTimerCallBack(self.nextDelterTime, 0, self.onTime, "ceshiOnTimer")


    def onTime(self, tid, *args):
        print("TimeLine", tid, *args)
        self.updateTimerId = 0
        delete = []
        for uuid, timeline in self.timeLines.items():
            timeline.tick()
            if timeline.isFinish():
                delete.append(uuid)
        for uuid in delete:
            self.timeLines[uuid].onEnd()
            del self.timeLines[uuid]
        self.nextDelterTime = self.getNextTimer()
        if self.nextDelterTime < float('inf'):
            self.updateTimerId = self.owner.addTimerCallBack(self.nextDelterTime, 0, self.onTime)

       
    def getNextTimer(self):
        minDelter = float('inf')
        for _, timeline in self.timeLines.items():
            if timeline.getNextDelterTime() < minDelter:
                minDelter = timeline.getNextDelterTime()
        return minDelter




