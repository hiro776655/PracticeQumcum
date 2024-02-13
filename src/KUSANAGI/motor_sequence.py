#coding: UTF-8

import qumcum_ble as qumcum
import copy
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
        # 現在のモーター角度
        self._crntCmdMotorPos = copy.deepcopy(defines.STANDING_POS)
        # 現在のモーター調整値
        self._caribOffset = copy.deepcopy(defines.CARIB_OFFSET_DEFAULT)

# publib

    def PowerOn(self) -> None:
        # モーター電源ON -> 直立姿勢
        start_time_sec = 1
        qumcum.motor_power_on(start_time_sec*1000)
        qumcum.wait(start_time_sec)

    def PowerOff(self) -> None:
        # モーター電源OFF 
        qumcum.motor_power_off()
    
    def GetCurrentPose(self, motor_no:EMotorNo=None) -> dict[EMotorNo,int]|int:
        if motor_no is None:
            return self._crntCmdMotorPos
        else:
            return self._crntCmdMotorPos[motor_no]
        
    def GetCaribOffset(self, motor_no:EMotorNo=None) -> dict[EMotorNo,int]|int:
        if motor_no is None:
            return self._caribOffset
        else:
            return self._caribOffset[motor_no]
    
    def SetCaribOffset(self, carib_offset:dict[EMotorNo,int]) -> None:
        self._caribOffset = copy.deepcopy(carib_offset)

    def Rotate(self, motor_no:EMotorNo, angle:int, time_ms:int, no_wait:bool=False) -> None:
        """
        モーターを1軸回転させる
        Args:
            motor_no:    指定
            angle:      0~180度(足回りは60~120)
            time_ms:    動作時間
            no_wait:    回転終了まで待機するか
        """
        clipped = self._clipAngle(motor_no, angle)
        adjusted = self._addCaribOffset(motor_no, clipped)
        qumcum.motor_angle_time(motor_no.value, adjusted, time_ms)
        qumcum.motor_start(no_wait)
        self._crntCmdMotorPos[motor_no] = clipped
    
    def RotateAdd(self, motor_no:EMotorNo, delta:int, time_ms:int, no_wait:bool=False) -> None:
        """モーターを1軸、現在値から回転増加させる

        Args:
            motor_no (EMotorNo): モーター軸
            delta (int): 増加分の回転角度[度]
            time_ms (int): 駆動時間[msec]
            no_wait (bool, optional): true=非同期、false=同期待ち. Defaults to False.
        """
        value = self._crntCmdMotorPos[motor_no] + delta
        self.Rotate(motor_no, value, time_ms, no_wait)


    def RotateMulti(self, motor_angle:dict[EMotorNo,int], time_ms:int, no_wait:bool=False) -> None:
        """
        モーターを複数軸回転させる
        Args:
            motorNo:    指定
            angle:      0~180度(足回りは60~120)
            time_ms:    動作時間
            no_wait:    回転終了まで待機するか
        """
        angles = copy.deepcopy(self._crntCmdMotorPos)
        for motor_no in EMotorNo:
            if motor_no in motor_angle:
                clipped = self._clipAngle(motor_no, motor_angle[motor_no])
                self._crntCmdMotorPos[motor_no] = clipped
                adjusted = self._addCaribOffset(motor_no, clipped)
                angles[motor_no] = adjusted
            else:
                adjusted = self._addCaribOffset(motor_no, angles[motor_no])
                angles[motor_no] = adjusted
        qumcum.motor_angle_multi_time(
            angles[EMotorNo.R_ARM], angles[EMotorNo.R_LEG], angles[EMotorNo.R_ANKL], 
            angles[EMotorNo.HEAD], angles[EMotorNo.L_ANKL], angles[EMotorNo.L_LEG], 
            angles[EMotorNo.L_ARM], time_ms)
        qumcum.motor_start(no_wait)
        pass

    def Adjust(self, motor_no: EMotorNo, delta:int) -> None:
        """
        モーター位置調整用
        """
        self._caribOffset[motor_no] = self._caribOffset[motor_no] + delta
        # motor_adjustでは 10 = 1° となる
        angle = (10 * self.GetCurrentPose(motor_no)) + self.GetCaribOffset(motor_no)
        qumcum.motor_adjust(motor_no.value, angle)
        qumcum.motor_start(no_wait=False)

# private

    def _clipAngle(self, motor_no:EMotorNo, angle:int) -> int:
        """モーター軸ごとの角度限界にクリップ

        Args:
            motor_no (EMotorNo): モーター軸
            angle (int): 回転角度

        Returns:
            int: モーター軸ごとの範囲内角度
        """
        if angle < self.ROTATE_RANGE[motor_no][0]:
            angle = self.ROTATE_RANGE[motor_no][0]
        elif angle > self.ROTATE_RANGE[motor_no][1]:
            angle = self.ROTATE_RANGE[motor_no][1]
        return angle
    
    def _addCaribOffset(self, motor_no:EMotorNo, angle:int) -> int:
        value = angle + int(self._caribOffset[motor_no]/10)
        return value

    def _updateCurrentPos(self, motor_no:EMotorNo, angle:int) -> int:
        value = self._clipAngle(motor_no, angle)
        self._crntCmdMotorPos[motor_no] = value
        return value