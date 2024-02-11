#coding: UTF-8

import asyncio
import qumcum_ble as qumcum
import KUSANAGI.defines as defines
from KUSANAGI.motor_sequence import MotorSequence

class QumcumController:
    CONNECT_ID = 'B652'

    @property
    def motorSeq(self):
        return self._motorSeq

    def __init__(self) -> None:
        self.Start()

    def __del__(self) -> None:
        self.End()

    def Start(self) -> None:
        qumcum.connect(self.CONNECT_ID)
        self._motorSeq = MotorSequence()
        self._motorSeq.PowerOn()
    
    def End(self) -> None:
        self._motorSeq.PowerOff()
        # Qumcumから切断
        qumcum.end()
    
    def AdjustDefaltPosition(self) -> None:
        """
        起動時に直立姿勢になるように自動調整
        ・電源ON後1回のみでよい
        """
        self.motorSeq.Adjust(defines.EMotorNo.R_ARM, 0.0)
        self.motorSeq.Adjust(defines.EMotorNo.R_LEG, 0.0)
        self.motorSeq.Adjust(defines.EMotorNo.R_ANKL, 0.0)
        self.motorSeq.Adjust(defines.EMotorNo.HEAD, 0.0)
        self.motorSeq.Adjust(defines.EMotorNo.L_ANKL, 0.0)
        self.motorSeq.Adjust(defines.EMotorNo.L_LEG, 0.0)
        self.motorSeq.Adjust(defines.EMotorNo.L_ARM, 0.0)
    
    def Standing(self):
        self._motorSeq.RotateMulti(defines.STANDING_POS, 500)
