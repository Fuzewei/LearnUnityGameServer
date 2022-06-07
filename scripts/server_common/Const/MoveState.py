# -*- coding: utf-8 -*-
import KBEngine
import GlobalConst
from KBEDebug import * 


# ai行为模式
class SERVER_MOVING_STAGE:
    IDLE = 0
    RANDOM_MOVE = 1 
    ROOTMOTION = 2
    CHAST_RUN = 3
    USING_SKILL = 4
    BE_ATTACK = 4

#行为树调用函数0=BT_INVALID,1=BT_SUCCESS,2=BT_FAILURE,3=BT_RUNNING
class AI_RESULT:
    BT_INVALID = 0
    BT_SUCCESS = 1 
    BT_FAILURE = 2
    BT_RUNNING = 3 


#移动类型
class CLIENT_MOVE_CONST:
    Idel = 0
    Walk = 1 
    Run = 2
    ServerMove = 6