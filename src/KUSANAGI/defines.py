#coding: UTF-8

from enum import Enum

class EMotorNo(Enum):
    R_ARM = 1
    R_LEG = 2
    R_ANKL = 3
    HEAD = 4
    L_ANKL = 5
    L_LEG = 6
    L_ARM = 7

STANDING_POS = { 
    EMotorNo.R_ARM:     0,
    EMotorNo.R_LEG:     90,
    EMotorNo.R_ANKL:    90,
    EMotorNo.HEAD:      90,
    EMotorNo.L_ANKL:    90,
    EMotorNo.L_LEG:     90,
    EMotorNo.L_ARM:     180,
    }