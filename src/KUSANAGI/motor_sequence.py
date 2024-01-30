#coding: UTF-8

import qumcum_ble as qumcum
import KUSANAGI.defines as defines
from KUSANAGI.defines import EMotorNo

"""
モーター1 :右腕     :上180、下0
モーター2 :右足     :外回転120、内回転60
モーター3 :右足首   :外傾き120、内傾き60
モーター4 :頭       :左180、右0
モーター5 :左足首   :外傾き60、内傾き120
モーター6 :左足     :外回転60、内回転120
モーター7 :左腕     :上0、下180
"""

class MotorSequence:
    ROTATE_RANGE = { 
        EMotorNo.R_ARM:     (0, 180),
        EMotorNo.R_LEG:     (60, 120),
        EMotorNo.R_ANKL:    (60, 120),
        EMotorNo.HEAD:      (0, 180),
        EMotorNo.L_ANKL:    (60, 120),
        EMotorNo.L_LEG:     (60, 120),
        EMotorNo.L_ARM:     (0, 180),
    }

    def __init__(self) -> None:
        # qumcum.get_motor_positionsが現在実装されていないため自前で保持
        self._prevCmdMotorPos = defines.STANDING_POS

    def PowerOn(self) -> None:
        # モーター電源ON -> 直立姿勢
        qumcum.motor_power_on(500)

    def PowerOff(self) -> None:
        # モーター電源OFF 
        qumcum.motor_power_off()
    
    def Standing(self, time_ms:int=500, no_wait:bool=False) -> None:
        pos = { 
            EMotorNo.R_ARM:     0,
            EMotorNo.R_LEG:     90,
            EMotorNo.R_ANKL:    90,
            EMotorNo.HEAD:      90,
            EMotorNo.L_ANKL:    90,
            EMotorNo.L_LEG:     90,
            EMotorNo.L_ARM:     180,
        }
        self.RotateMulti(pos, time_ms, no_wait)

    def Rotate(self, motor_no:EMotorNo, angle:int, time_ms:int, no_wait:bool=False) -> None:
        """
        モーターを1軸回転させる
        Args:
            motor_no:    指定
            angle:      0~180度(足回りは60~120)
            time_ms:    動作時間
            no_wait:    回転終了まで待機するか
        """
        angle = self._clipAngle(motor_no, angle)
        qumcum.motor_angle_time(motor_no.value, angle, time_ms)
        qumcum.motor_start(no_wait)
        self._prevCmdMotorPos[motor_no] = angle

    def RotateMulti(self, motor_angle:dict[EMotorNo,int], time_ms:int, no_wait:bool=False) -> None:
        """
        モーターを複数軸回転させる
        Args:
            motorNo:    指定
            angle:      0~180度(足回りは60~120)
            time_ms:    動作時間
            no_wait:    回転終了まで待機するか
        """
        angles = self._prevCmdMotorPos
        for motorNo in EMotorNo:
            if motorNo in motor_angle:
                angles[motorNo] = self._clipAngle(motorNo, motor_angle[motorNo])
        qumcum.motor_angle_multi_time(angles[EMotorNo.R_ARM], angles[EMotorNo.R_LEG], angles[EMotorNo.R_ANKL], 
            angles[EMotorNo.HEAD], angles[EMotorNo.L_ANKL], angles[EMotorNo.L_LEG], angles[EMotorNo.L_ARM], time_ms)
        qumcum.motor_start(no_wait)
        pass

    def _clipAngle(self, motorNo:EMotorNo, angle:int) -> int:
        if angle < self.ROTATE_RANGE[motorNo][0]:
            angle = self.ROTATE_RANGE[motorNo][0]
        elif angle > self.ROTATE_RANGE[motorNo][1]:
            angle = self.ROTATE_RANGE[motorNo][1]
        return angle