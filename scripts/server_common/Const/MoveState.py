# -*- coding: utf-8 -*-
import KBEngine
import GlobalConst
from KBEDebug import * 


# 移动状态定义

IDLE = 0


# 服务端移动模式
class SERVER_MOVING_STAGE:
    IDLE = 0
    RANDOM_MOVE = 1 
    ROOTMOTION = 2

class AI_RESULT:
    BT_INVALID = 0
    BT_SUCCESS = 1 
    BT_FAILURE = 2
    BT_RUNNING = 3 
#行为树调用函数0=BT_INVALID,1=BT_SUCCESS,2=BT_FAILURE,3=BT_RUNNING

class CLIENT_MOVE_CONST:
    Idel = 0
    Walk = 1 