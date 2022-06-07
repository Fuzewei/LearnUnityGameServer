from SkillManager.timeLineNodes.CommonAttackNode import CommonAttackNode
from SkillManager.timeLineNodes.PlayerAnimationNode import PlayerAnimationNode 
from SkillManager.timeLineNodes.StartNewTimeLine import StartNewTimeLine 
from SkillManager.timeLineNodes.TimeLineEndNode import TimeLineEndNode
from SkillManager.SkillTimeLine import SkillTimeLine


class SkillFactory:
    def __init__(self):
        pass

    def getSkillBeginTimeLine(self, skillId): 
        timeLine = SkillTimeLine()
        node1 = PlayerAnimationNode(0, "123")
        timeLine.addNode(node1)
        node2 = CommonAttackNode(0.3)
        timeLine.addNode(node2)
        node4 = StartNewTimeLine(1)
        timeLine.addNode(node4)
        node3 = TimeLineEndNode(2)
        timeLine.addNode(node3) 
        return timeLine
