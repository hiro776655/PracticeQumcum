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
        self._crntCmdMotorPos = defines.STANDING_POS

# publib

    def PowerOn(self) -> None:
        # モーター電源ON -> 直立姿勢
        qumcum.motor_power_on(1000)

    def PowerOff(self) -> None:
        # モーター電源OFF 
        qumcum.motor_power_off()
    
    def GetCurrentPos(self, motor_no:EMotorNo=None) -> dict[EMotorNo,float]|float:
        if motor_no is None:
            return self._crntCmdMotorPos
        else:
            return self._crntCmdMotorPos[motor_no]

    def Rotate(self, motor_no:EMotorNo, angle:float, time_ms:int, no_wait:bool=False) -> None:
        """
        モーターを1軸回転させる
        Args:
            motor_no:    指定
            angle:      0~180度(足回りは60~120)
            time_ms:    動作時間
            no_wait:    回転終了まで待機するか
        """
        angle = self._convertAngle(motor_no, angle)
        qumcum.motor_angle_time(motor_no.value, angle, time_ms)
        qumcum.motor_start(no_wait)
        self._crntCmdMotorPos[motor_no] = angle
    
    def RoateAdd(self, motor_no:EMotorNo, delta:float, time_ms:int, no_wait:bool=False) -> None:
        """モーターを1軸、現在値から回転増加させる

        Args:
            motor_no (EMotorNo): モーター軸
            delta (float): 増加分の回転角度[度]
            time_ms (int): 駆動時間[msec]
            no_wait (bool, optional): true=非同期、false=同期待ち. Defaults to False.
        """
        angle = self._moveCurrentPos(motor_no, delta)
        self.Rotate(motor_no, angle, time_ms, no_wait)


    def RotateMulti(self, motor_angle:dict[EMotorNo,float], time_ms:int, no_wait:bool=False) -> None:
        """
        モーターを複数軸回転させる
        Args:
            motorNo:    指定
            angle:      0~180度(足回りは60~120)
            time_ms:    動作時間
            no_wait:    回転終了まで待機するか
        """
        angles = self._crntCmdMotorPos
        for motor_no in EMotorNo:
            if motor_no in motor_angle:
                angle = self._convertAngle(motor_no, motor_angle[motor_no])
                angles[motor_no] = angle
        qumcum.motor_angle_multi_time(
            angles[EMotorNo.R_ARM], angles[EMotorNo.R_LEG], angles[EMotorNo.R_ANKL], 
            angles[EMotorNo.HEAD], angles[EMotorNo.L_ANKL], angles[EMotorNo.L_LEG], 
            angles[EMotorNo.L_ARM], time_ms)
        qumcum.motor_start(no_wait)
        pass

    def Adjust(self, motor_no: EMotorNo, delta:float) -> None:
        """
        モーター位置調整用
        """
        angle = self._moveCurrentPos(motor_no, delta)
        qumcum.motor_adjust(motor_no.value, angle)
        qumcum.motor_start(no_wait=False)

# private
        
    def _convertAngle(self, motor_no:EMotorNo, angle:float) -> float:
        value = self._clipAngle(motor_no, angle)
        # value = self._alignAngleDirection(motor_no, value)
        return value

    def _clipAngle(self, motor_no:EMotorNo, angle:float) -> float:
        """モーター軸ごとの角度限界にクリップ

        Args:
            motor_no (EMotorNo): モーター軸
            angle (float): 回転角度

        Returns:
            float: モーター軸ごとの範囲内角度
        """
        if angle < self.ROTATE_RANGE[motor_no][0]:
            angle = self.ROTATE_RANGE[motor_no][0]
        elif angle > self.ROTATE_RANGE[motor_no][1]:
            angle = self.ROTATE_RANGE[motor_no][1]
        return angle
    
    def _alignAngleDirection(self, motor_no:EMotorNo, angle:float) -> float:
        """モータ軸の向きの違いからくる正負の向きを統一する

        Args:
            motor_no (EMotorNo): モーター軸
            angle (float): 回転角度

        Returns:
            float: 右半身の向きに合わせた回転角度
        """
        if motor_no == EMotorNo.L_ARM \
        or motor_no == EMotorNo.L_ANKL \
        or motor_no == EMotorNo.L_LEG :
            return (90 - angle) + 90
        else :
            return angle

    def _updateCurrentPos(self, motor_no:EMotorNo, angle:float) -> float:
        value = self._clipAngle(motor_no, angle)
        self._crntCmdMotorPos[motor_no] = value
        return value
    
    def _moveCurrentPos(self, motor_no:EMotorNo, delta:float) -> float:
        angle = self._crntCmdMotorPos[motor_no] + delta
        angle = self._updateCurrentPos(motor_no, angle)
        return angle