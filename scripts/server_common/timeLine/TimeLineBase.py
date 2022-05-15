# -*- coding: utf-8 -*-
import time


class TimeLineBase():
    def __init__(self):
        self.uuid = None
        self.tickTimeStamp = None
        self.nextIndex = 0
        self.delterTimeStamp = None
        self.nodesList = []
        self.speed = 1
        self.manager = None

    def reset(self, manager, uuid):
        self.manager = manager
        self.uuid = uuid
        self.delterTimeStamp = 0

    def start(self):
        self.tickTimeStamp = time.time()
        self.setSpeed(1)
        if self.getNextDelterTime() == 0:
            self.tick()

    def tick(self):
        now = time.time()
        self.delterTimeStamp += (now - self.tickTimeStamp) * self.speed
        self.tickTimeStamp = now
        print("TimeLineBase.tick", now)
        if not self.isFinish():
            self.doTick(self.nextIndex)
            self.nextIndex += 1

    def doTick(self, index):
        self.nodesList[index].run()

    def isFinish(self):
        return len(self.nodesList) <= self.nextIndex

    def setSpeed(self, newspeed):
        self.speed = newspeed

    #下一次tick到当前时间的时间差
    def getNextDelterTime(self):
        _t = self.__getNextTimeStamp() - self.delterTimeStamp
        return _t/self.speed

    def onEnd(self):
        print("TimeLineBase.onEnd")
        for node in self.nodesList:
            node.OnDestory()
        self.nodesList = []
    
    def addNode(self, node):
        node.owneTimeLine = self
        node.OnSetTimeLine()
        i = 0
        for _node in self.nodesList:
            if _node.runTimeStamp >= node.runTimeStamp:
                break
            else:   
                i += 1
        node.nodeId = i
        self.nodesList.insert(i, node)

    def __getNextTimeStamp(self):
        return self.nodesList[self.nextIndex].runTimeStamp