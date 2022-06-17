from ast import If
from SkillManager.timeLineNodes.CommonAttackNode import CommonAttackNode
from SkillManager.timeLineNodes.PlayerAnimationNode import PlayerAnimationNode 
from SkillManager.timeLineNodes.StartNewSkill import StartNewSkill 
from SkillManager.timeLineNodes.TimeLineEndNode import TimeLineEndNode
from SkillManager.SkillTimeLine import SkillTimeLine


class SkillFactory:
    def __init__(self):
        pass

    def getSkillBeginTimeLine(self, timeLineId): 
        timeLine = SkillTimeLine()
        if  timeLineId == 1:
            node1 = PlayerAnimationNode(0, "123")
            timeLine.addNode(node1)
            node2 = CommonAttackNode(0.3)
            timeLine.addNode(node2)
            node4 = StartNewSkill(1.0, 0.4, 2)
            timeLine.addNode(node4)
            node3 = TimeLineEndNode(2.0)
            timeLine.addNode(node3)
        elif timeLineId == 2:
            node1 = PlayerAnimationNode(0, "123")
            timeLine.addNode(node1)
            node2 = CommonAttackNode(0.3)
            timeLine.addNode(node2)
            node4 = StartNewSkill(0.8, 0.4, 3)
            timeLine.addNode(node4)
            node3 = TimeLineEndNode(2.0)
            timeLine.addNode(node3)
        elif timeLineId == 3:
            node1 = PlayerAnimationNode(0, "123")
            timeLine.addNode(node1)
            node2 = CommonAttackNode(0.6)
            timeLine.addNode(node2)
            node3 = TimeLineEndNode(2.0)
            timeLine.addNode(node3)
        return timeLine
