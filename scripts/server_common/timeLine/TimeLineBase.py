# -*- coding: utf-8 -*-
import time


class TimeLineBase():
    def __init__(self):
        self.tickTimeStamp = None
        self.nextIndex = 0
        self.delterTimeStamp = 0
        self.nodesList = []
        self.speed = 1
        self.manager = None

    def setManager(self, manager):
        self.manager = manager

    def start(self):
        self.tickTimeStamp = time.time()
        self.setSpeed(1)
        self.tick()

    def tick(self):
        now = time.time()
        self.delterTimeStamp += (now - self.tickTimeStamp) * self.speed
        while not self.isFinish() and self.delterTimeStamp >= self.getNextTimeStamp():
            self.doTick()
            self.nextIndex += 1
        self.tickTimeStamp = now


    def doTick(self):
        self.nodesList[self.nextIndex].run()

    def isFinish(self):
        return len(self.nodesList) <= self.nextIndex

    def setSpeed(self, newspeed):
        self.speed = newspeed

    def getNextTimeStamp(self):
        return self.nodesList[self.nextIndex].runTimeStamp

    #下一次tick到当前时间的时间差
    def getNextDelterTime(self):
        _t = self.getNextTimeStamp() - self.delterTimeStamp
        return _t/self.speed


    def onEnd(self):
        print("TimeLineBase.onEnd")
    
    def addNode(self, node):
        node.owneTimeLine = self
        node.OnSetTimeLine()
        i = 0
        for _node in self.nodesList:
            if _node.runTimeStamp >= node.runTimeStamp:
                break
            else:   
                i += 1
        self.nodesList.insert(i, node)

