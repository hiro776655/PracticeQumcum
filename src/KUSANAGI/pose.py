#coding: UTF-8

from __future__ import annotations
import copy
from KUSANAGI.defines import EMotorNo

class Pose:
    def __init__(self, pose:Pose=None) -> None:
        self.head = 0
        self.r_arm = 0
        self.r_leg = 0
        self.r_ankle = 0
        self.l_arm = 0
        self.l_leg = 0
        self.l_ankle = 0
        if pose is not None:
            self.SetPose(pose)
    
    def Get(self, motor_no:EMotorNo) -> int:
        if motor_no == EMotorNo.HEAD:
            return self.head
        elif motor_no == EMotorNo.R_ARM:
            return self.r_arm
        elif motor_no == EMotorNo.R_LEG:
            return self.r_leg
        elif motor_no == EMotorNo.R_ANKL:
            return self.r_ankle
        elif motor_no == EMotorNo.L_ARM:
            return self.l_arm
        elif motor_no == EMotorNo.L_LEG:
            return self.l_leg
        elif motor_no == EMotorNo.L_ANKL:
            return self.l_ankle
    
    def Set(self, motor_no:EMotorNo, value:int) -> None:
        if motor_no == EMotorNo.HEAD:
            self.head = value
        elif motor_no == EMotorNo.R_ARM:
            self.r_arm = value
        elif motor_no == EMotorNo.R_LEG:
            self.r_leg = value
        elif motor_no == EMotorNo.R_ANKL:
            self.r_ankle = value
        elif motor_no == EMotorNo.L_ARM:
            self.l_arm = value
        elif motor_no == EMotorNo.L_LEG:
            self.l_leg = value
        elif motor_no == EMotorNo.L_ANKL:
            self.l_ankle = value

    def SetPose(self, pose:Pose) -> None:
        self.head = pose.head
        self.r_arm = pose.r_arm
        self.r_leg = pose.r_leg
        self.r_ankle = pose.r_ankle
        self.l_arm = pose.l_arm
        self.l_leg = pose.l_leg
        self.l_ankle = pose.l_ankle
    
    def deepcopy(self) -> Pose:
        return copy.deepcopy(self)
