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
        qumcum.connect(self.CONNECT_ID)
        self._motorSeq = MotorSequence()
        self._motorSeq.PowerOn()

    def __del__(self):
        self._motorSeq.PowerOff()
        # Qumcumから切断
        qumcum.end()
    
    def Standing(self):
        self._motorSeq.RotateMulti(defines.STANDING_POS, 500)
