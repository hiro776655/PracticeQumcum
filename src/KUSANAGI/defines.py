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

CARIB_OFFSET_DEFAULT = { 
    EMotorNo.R_ARM:     0,
    EMotorNo.R_LEG:     0,
    EMotorNo.R_ANKL:    0,
    EMotorNo.HEAD:      0,
    EMotorNo.L_ANKL:    0,
    EMotorNo.L_LEG:     0,
    EMotorNo.L_ARM:     0,
    }

MOTOR_ROTATE_RANGE = { 
        EMotorNo.R_ARM:     (0, 180),
        EMotorNo.R_LEG:     (60, 120),
        EMotorNo.R_ANKL:    (60, 120),
        EMotorNo.HEAD:      (0, 180),
        EMotorNo.L_ANKL:    (60, 120),
        EMotorNo.L_LEG:     (60, 120),
        EMotorNo.L_ARM:     (0, 180),
    }