import xml.etree.ElementTree as et
from SkillManager.timeLineNodes.CommonAttackNode import CommonAttackNode
from SkillManager.timeLineNodes.PlayerAnimationNode import PlayerAnimationNode 
from SkillManager.timeLineNodes.StartNewSkill import StartNewSkill 
from SkillManager.timeLineNodes.TimeLineEndNode import TimeLineEndNode
from SkillManager.SkillTimeLine import SkillTimeLine
import KBEngine

class XmlSkillLogicName:
    
    def __init__(self):
        self.name = None
        self.beginTime = 0.0
        self.endTime = 0.0
        self.skillParams = {}
        
    def fromXmlAttr(self, node):
        self.name = node.tag
        self.beginTime = float(node.find("beginTime").text)
        self.endTime = float(node.find("endTime").text)
        for paramNode in node.find("params"):
            self.skillParams[paramNode.tag] = paramNode.text
       
class XmlSkillTimeLine:
    
    def __init__(self):
        self.name = None
        self.node = []
        
    def fromXmlAttr(self, node):
        self.name = node.tag
        for subNode in node.find("nodes"):
            node = XmlSkillLogicName()
            node.fromXmlAttr(subNode)
            self.node.append(node)


__SkillData = {}
def initSkillData(fileName = "MoveInfo/SkillTimeLine.xml"):
    if __SkillData:
        return __SkillData
    SkillTimeLinePath = KBEngine.matchPath(fileName)
    tree = et.parse(SkillTimeLinePath)
    root = tree.getroot()
    for skillNameNode in root:
        timeLine = XmlSkillTimeLine()
        timeLine.fromXmlAttr(skillNameNode)
        __SkillData[skillNameNode.tag] = timeLine
    return __SkillData

#initSkillData()



class SkillFactory:
    
    skillNodes = {
        "CommonAttackNode" : CommonAttackNode,
        "PlayerAnimationNode" : PlayerAnimationNode,
        "StartNewSkill" : StartNewSkill,
        "TimeLineEndNode" : TimeLineEndNode,
    }
    
    def __init__(self):
        initSkillData()
        pass
    
    def getSkillBeginTimeLine(self, timeLineName): 
        timeLineData = initSkillData()[timeLineName]
        timeLine = SkillTimeLine()
        for logicNode in timeLineData.node:
            node = SkillFactory.skillNodes[logicNode.name](logicNode)
            timeLine.addNode(node)
        return timeLine
        
        
        
        # timeLine = SkillTimeLine()
        # if  timeLineId == 1:
        #     node1 = PlayerAnimationNode(0, "123")
        #     timeLine.addNode(node1)
        #     node2 = CommonAttackNode(0.3)
        #     timeLine.addNode(node2)
        #     node4 = StartNewSkill(1.0, 0.4, 2)
        #     timeLine.addNode(node4)
        #     node3 = TimeLineEndNode(2.0)
        #     timeLine.addNode(node3)
        # elif timeLineId == 2:
        #     node1 = PlayerAnimationNode(0, "123")
        #     timeLine.addNode(node1)
        #     node2 = CommonAttackNode(0.3)
        #     timeLine.addNode(node2)
        #     node4 = StartNewSkill(0.8, 0.4, 3)
        #     timeLine.addNode(node4)
        #     node3 = TimeLineEndNode(2.0)
        #     timeLine.addNode(node3)
        # elif timeLineId == 3:
        #     node1 = PlayerAnimationNode(0, "123")
        #     timeLine.addNode(node1)
        #     node2 = CommonAttackNode(0.6)
        #     timeLine.addNode(node2)
        #     node3 = TimeLineEndNode(2.0)
        #     timeLine.addNode(node3)
        # return timeLine
