# -*- coding: utf-8 -*-
import time
import KBEngine

class TimeLineManager():
    def __init__(self, owner):
        self.owner = owner
        self.nodeUUid = 100000
        self.timeLines = {}
        self.nextDelterTime = float('inf')
        self.nextTimeLineUuid = None #下次触发的uuid
        self.updateTimerId = 0

    
    def getUUid(self):
        a = self.nodeUUid
        self.nodeUUid += 1
        return a 

    def getTimeLine(self, uuid):
        return  self.timeLines[uuid]

    def addTimeLine(self, uuid, timeline):
        timeline.reset(self, uuid)
        timeline.start()
        if timeline.isFinish():
            return
        self.timeLines[uuid] = timeline
        if timeline.getNextDelterTime() < self.nextDelterTime:
            if self.updateTimerId > 0 :
                self.owner.delTimerCallBack(self.updateTimerId)
            self.nextDelterTime = timeline.getNextDelterTime()
            self.nextTimeLineUuid = timeline.uuid
            self.updateTimerId = self.owner.addTimerCallBack(self.nextDelterTime, 0, self.onTime)

    def delTimeLine(self, uuid, timeline):
        tickTimeLine = self.timeLines[uuid]
        if not tickTimeLine:
            return
        tickTimeLine.onEnd()
        del self.timeLines[uuid]
        if uuid == self.nextTimeLineUuid:
            self.owner.delTimerCallBack(self.updateTimerId)
            self.updateTimerId = 0
            self.nextDelterTime, self.nextTimeLineUuid = self.getNextTimeLine()
            if self.nextDelterTime < float('inf'):
                self.updateTimerId = self.owner.addTimerCallBack(self.nextDelterTime, 0, self.onTime)


    def onTime(self, tid, *args):
        print("TimeLine", self.nextDelterTime, self.nextTimeLineUuid)
        self.updateTimerId = 0
        deleteUUids = []
        tickTimeLine = self.timeLines[self.nextTimeLineUuid]
        tickTimeLine.tick()
        if tickTimeLine.isFinish():
            deleteUUids.append(tickTimeLine.uuid)
        for uuid in deleteUUids:
            self.timeLines[uuid].onEnd()
            del self.timeLines[uuid]
    

        self.nextDelterTime, self.nextTimeLineUuid = self.getNextTimeLine()
        if self.nextDelterTime < float('inf'):
            self.updateTimerId = self.owner.addTimerCallBack(self.nextDelterTime, 0, self.onTime)

       
    def getNextTimeLine(self):
        minDelter = float('inf')
        timeLineUUid = None
        for _, timeline in self.timeLines.items():
            if timeline.getNextDelterTime() < minDelter:
                minDelter = timeline.getNextDelterTime()
                timeLineUUid = timeline.uuid
        return minDelter, timeLineUUid



