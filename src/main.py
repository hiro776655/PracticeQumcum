#coding: UTF-8

import keyboard as kb
from KUSANAGI.qumcum_controller import QumcumController
from KUSANAGI.motor_sequence import MotorSequence
import qumcum_ble as qumcum
from KUSANAGI.defines import EMotorNo
from KUSANAGI.keyboard_listener import KeyboardListener

"""
注意点
・ホストPCの設定でBluetooth のペアリングは不要
・qumcum_bleのモーターへの命令は同期/非同期の両方可能(motor_startの引数で変わる)
・モーターOFFにするのは電池消費削減のため
・モーターON時の動作時間はあくまで初期値で、別途指定した場合は上書きされる(motor_angle_multi_timeのあとに)
・モーターの動作途中で、次の命令が届くと前の命令の動作時間内で新たな命令位置へ動作しようとする。
  例: 500msecで右腕90度の位置に命令した後、400msec時点で500msecで右腕180度の位置に命令すると動作時間100msecで2番目の命令を実行しようとする
・連続でコマンドを発行しても、大体120msec程度の通信コストがある

motor_power_onでの初期姿勢調整
  https://personal.qumcum.com/robo_adjust/

Receive dataの読み方
  @,＜内部管理用番号＞,＜バッテリ残量の目安＞,＜超音波距離センサの計測値＞,＜マイクの計測値＞

疑問点
・異なる軸のモーターへ非同期に命令を飛ばした場合、同時に動くのか？
"""


def main():
    motor = MotorSequence()
    motor.SetCaribOffset({ 
        EMotorNo.R_ARM:     280,
        EMotorNo.R_LEG:     20,
        EMotorNo.R_ANKL:    0,
        EMotorNo.HEAD:      220,
        EMotorNo.L_ANKL:    0,
        EMotorNo.L_LEG:     320,
        EMotorNo.L_ARM:     290,
    })

    qm = QumcumController(motor)
    qm.Start()
    qm.Standing()
    interface = KeyboardListener(qm)
    interface.Run()
    qm.End()


if __name__ == "__main__":
    main()