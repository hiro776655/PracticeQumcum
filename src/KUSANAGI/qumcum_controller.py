#coding: UTF-8

import asyncio
import qumcum_ble as qumcum
import KUSANAGI.defines as defines
from KUSANAGI.defines import EMotorNo
from KUSANAGI.motor_sequence import MotorSequence

class QumcumController:
    CONNECT_ID = 'B652'

    @property
    def motorSeq(self):
        return self._motorSeq

    def __init__(self, motorSeq:MotorSequence) -> None:
        self._motorSeq = motorSeq
        self._walkMoveTime = 400

    def __del__(self) -> None:
        self.End()

    def Start(self) -> None:
        qumcum.connect(self.CONNECT_ID)
        self.motorSeq.PowerOn()
    
    def End(self) -> None:
        self.motorSeq.PowerOff()
        # Qumcumから切断
        qumcum.end()
    
    def Standing(self):
        self.motorSeq.RotateMulti(defines.STANDING_POS, 500, False)
    
    def MaeNarae(self):
        self.motorSeq.RotateMulti({
            EMotorNo.R_ARM: 90,
            EMotorNo.R_LEG: 90,
            EMotorNo.R_ANKL: 90,
            EMotorNo.HEAD: 90,
            EMotorNo.L_ANKL: 90,
            EMotorNo.L_LEG: 90,
            EMotorNo.L_ARM: 90,
        }, 500, False)

    def RightFootStanding(self):
        """右足立ち
        """
        self.motorSeq.Rotate(EMotorNo.L_ANKL, 70, self._walkMoveTime, False)
        self.motorSeq.Rotate(EMotorNo.R_ANKL, 108, self._walkMoveTime, False)
        self.motorSeq.RotateMulti({
            EMotorNo.L_LEG: 90,
            EMotorNo.R_LEG: 90,
        }, self._walkMoveTime, False)

    def LeftFootStanding(self):
        """左足立ち
        """
        self.motorSeq.Rotate(EMotorNo.R_ANKL, 110, self._walkMoveTime, False)
        self.motorSeq.Rotate(EMotorNo.L_ANKL, 70, self._walkMoveTime, False)
        self.motorSeq.RotateMulti({
            EMotorNo.L_LEG: 90,
            EMotorNo.R_LEG: 90,
        }, self._walkMoveTime, False)
    
    def Walk(self):
        # 右足立ちになる
        self.RightFootStanding()
        # 左足一歩前に進める
        self.motorSeq.RotateMulti({
            EMotorNo.R_LEG: 70,
            EMotorNo.L_ANKL: 90,
            EMotorNo.L_LEG: 70,
        }, self._walkMoveTime, False)
        self.motorSeq.Rotate(EMotorNo.R_ANKL, 90, self._walkMoveTime, False)
        # 左足立ちになる
        self.LeftFootStanding()
        # 右足一歩前に進める
        self.motorSeq.RotateMulti({
            EMotorNo.L_LEG: 110,
            EMotorNo.R_ANKL: 90,
            EMotorNo.R_LEG: 110,
        }, self._walkMoveTime, False)
        self.motorSeq.Rotate(EMotorNo.L_ANKL, 90, self._walkMoveTime, False)
    
    def WalkStop(self):
        # 右足立ちになる
        self.RightFootStanding()
        # 直立
        self.Standing()
    
    def BackWalk(self):
        # 右足立ちになる
        self.RightFootStanding()
        # 左足一歩後ろに進める
        self.motorSeq.RotateMulti({
            EMotorNo.R_LEG: 110,
            EMotorNo.L_ANKL: 90,
            EMotorNo.L_LEG: 110,
        }, self._walkMoveTime, False)
        self.motorSeq.Rotate(EMotorNo.R_ANKL, 90, self._walkMoveTime, False)
        # 左足立ちになる
        self.LeftFootStanding()
        # 右足一歩後ろに進める
        self.motorSeq.RotateMulti({
            EMotorNo.L_LEG: 70,
            EMotorNo.R_ANKL: 90,
            EMotorNo.R_LEG: 70,
        }, self._walkMoveTime, False)
        self.motorSeq.Rotate(EMotorNo.L_ANKL, 90, self._walkMoveTime, False)

    def TurnLeft(self):
        # 左足立ちになる
        self.LeftFootStanding()
        # 30°回転
        self.motorSeq.Rotate(EMotorNo.L_LEG, 120, self._walkMoveTime, False)
        # 右足おろす（両足が地面につく）
        self.motorSeq.RotateMulti({
            EMotorNo.L_ANKL: 90,
            EMotorNo.R_ANKL: 90,
        }, self._walkMoveTime, False)
        # 右足立ちになる
        self.RightFootStanding()
        # 左足向きをまっすぐ
        self.motorSeq.RotateMulti({
            EMotorNo.L_LEG: 90,
            EMotorNo.L_ANKL: 90,
        }, self._walkMoveTime, False)
        self.motorSeq.Rotate(EMotorNo.R_ANKL, 90, self._walkMoveTime, False)
    
    def TurnRight(self):
        # 右足立ちになる
        self.RightFootStanding()
        # 30°回転
        self.motorSeq.Rotate(EMotorNo.R_LEG, 60, self._walkMoveTime, False)
        # 左足おろす（両足が地面につく）
        self.motorSeq.RotateMulti({
            EMotorNo.L_ANKL: 90,
            EMotorNo.R_ANKL: 90,
        }, self._walkMoveTime, False)
        # 左足立ちになる
        self.LeftFootStanding()
        # 右足向きをまっすぐ
        self.motorSeq.RotateMulti({
            EMotorNo.R_LEG: 90,
            EMotorNo.R_ANKL: 90,
        }, self._walkMoveTime, False)
        self.motorSeq.Rotate(EMotorNo.L_ANKL, 90, self._walkMoveTime, False)
