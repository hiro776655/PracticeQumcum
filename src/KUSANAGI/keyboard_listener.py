#coding: UTF-8

import keyboard as kb
import time
import sys
from KUSANAGI.qumcum_controller import QumcumController
from KUSANAGI.defines import EMotorNo
import qumcum_ble

class InterfaceMode:
    def __init__(self, qumcum: QumcumController) -> None:
        self.qumcum = qumcum
        pass

    def Start(self) -> None:
        pass

    def Exit(self) -> None:
        pass



class AdjustMotorMode(InterfaceMode):
    def __init__(self, qumcum: QumcumController) -> None:
        super().__init__(qumcum)

    def Start(self) -> None:
        super().Start()
        repeatSuppression = False
        kb.add_hotkey('1+up', self._motorAdjust(EMotorNo.R_ARM, 10), suppress=repeatSuppression)
        kb.add_hotkey('2+up', self._motorAdjust(EMotorNo.R_LEG, 10), suppress=repeatSuppression)
        kb.add_hotkey('3+up', self._motorAdjust(EMotorNo.R_ANKL, 10), suppress=repeatSuppression)
        kb.add_hotkey('4+up', self._motorAdjust(EMotorNo.HEAD, 10), suppress=repeatSuppression)
        kb.add_hotkey('5+up', self._motorAdjust(EMotorNo.L_ANKL, 10), suppress=repeatSuppression)
        kb.add_hotkey('6+up', self._motorAdjust(EMotorNo.L_LEG, 10), suppress=repeatSuppression)
        kb.add_hotkey('7+up', self._motorAdjust(EMotorNo.L_ARM, 10), suppress=repeatSuppression)
        kb.add_hotkey('1+down', self._motorAdjust(EMotorNo.R_ARM, -10), suppress=repeatSuppression)
        kb.add_hotkey('2+down', self._motorAdjust(EMotorNo.R_LEG, -10), suppress=repeatSuppression)
        kb.add_hotkey('3+down', self._motorAdjust(EMotorNo.R_ANKL, -10), suppress=repeatSuppression)
        kb.add_hotkey('4+down', self._motorAdjust(EMotorNo.HEAD, -10), suppress=repeatSuppression)
        kb.add_hotkey('5+down', self._motorAdjust(EMotorNo.L_ANKL, -10), suppress=repeatSuppression)
        kb.add_hotkey('6+down', self._motorAdjust(EMotorNo.L_LEG, -10), suppress=repeatSuppression)
        kb.add_hotkey('7+down', self._motorAdjust(EMotorNo.L_ARM, -10), suppress=repeatSuppression)
        kb.add_hotkey('ctrl+1+up', self._motorAdjust(EMotorNo.R_ARM, 100), suppress=repeatSuppression)
        kb.add_hotkey('ctrl+2+up', self._motorAdjust(EMotorNo.R_LEG, 100), suppress=repeatSuppression)
        kb.add_hotkey('ctrl+3+up', self._motorAdjust(EMotorNo.R_ANKL, 100), suppress=repeatSuppression)
        kb.add_hotkey('ctrl+4+up', self._motorAdjust(EMotorNo.HEAD, 100), suppress=repeatSuppression)
        kb.add_hotkey('ctrl+5+up', self._motorAdjust(EMotorNo.L_ANKL, 100), suppress=repeatSuppression)
        kb.add_hotkey('ctrl+6+up', self._motorAdjust(EMotorNo.L_LEG, 100), suppress=repeatSuppression)
        kb.add_hotkey('ctrl+7+up', self._motorAdjust(EMotorNo.L_ARM, 100), suppress=repeatSuppression)
        kb.add_hotkey('ctrl+1+down', self._motorAdjust(EMotorNo.R_ARM, -100), suppress=repeatSuppression)
        kb.add_hotkey('ctrl+2+down', self._motorAdjust(EMotorNo.R_LEG, -100), suppress=repeatSuppression)
        kb.add_hotkey('ctrl+3+down', self._motorAdjust(EMotorNo.R_ANKL, -100), suppress=repeatSuppression)
        kb.add_hotkey('ctrl+4+down', self._motorAdjust(EMotorNo.HEAD, -100), suppress=repeatSuppression)
        kb.add_hotkey('ctrl+5+down', self._motorAdjust(EMotorNo.L_ANKL, -100), suppress=repeatSuppression)
        kb.add_hotkey('ctrl+6+down', self._motorAdjust(EMotorNo.L_LEG, -100), suppress=repeatSuppression)
        kb.add_hotkey('ctrl+7+down', self._motorAdjust(EMotorNo.L_ARM, -100), suppress=repeatSuppression)
        kb.add_hotkey('h', self._showKeyGuide)
        kb.add_hotkey('c', self._getCurrentCaribOffset)
        kb.add_hotkey('p', self._getCurrentPose)
        self._showKeyGuide()
        kb.wait('escape')
    
    def Exit(self) -> None:
        super().Exit()
        kb.clear_all_hotkeys()

    def _showKeyGuide(self) -> None:
        print('----- Adjust Motor Mode -----')
        print('[1 + arrow_up/down]:     Right Arm   +/-1')
        print('[2 + arrow_up/down]:     Right Leg   +/-1')
        print('[3 + arrow_up/down]:     Right Ankle +/-1')
        print('[4 + arrow_up/down]:     Head        +/-1')
        print('[5 + arrow_up/down]:     Left Ankle  +/-1')
        print('[6 + arrow_up/down]:     Left Leg    +/-1')
        print('[7 + arrow_up/down]:     Left Arm    +/-1')
        print('[c]:                     Show current carib offset')
        print('[p]:                     Show current pose')
        print('[esc]:                   Exit')

    def _motorAdjust(self, motorNo: EMotorNo, delta:int):
        def motorAdjust() -> None:
            self.qumcum.motorSeq.Adjust(motorNo, delta)
        return motorAdjust
    
    def _getCurrentCaribOffset(self):
        carib : dict[EMotorNo, int] = self.qumcum.motorSeq.GetCaribOffset()
        print('----- Carib Offset -----')
        for motor, value in carib.items():
            print(f'{motor.name}: {value}')
    
    def _getCurrentPose(self):
        pose : dict[EMotorNo, int] = self.qumcum.motorSeq.GetCurrentPose()
        print('----- Current Pose -----')
        for motor, value in pose.items():
            print(f'{motor.name}: {value}')



class ManualControlMode(InterfaceMode):
    def __init__(self, qumcum: QumcumController) -> None:
        super().__init__(qumcum)

    def Start(self) -> None:
        super().Start()
        repeatSuppression = False
        kb.add_hotkey('1+up', self._motorMove(EMotorNo.R_ARM, 10), suppress=repeatSuppression)
        kb.add_hotkey('2+up', self._motorMove(EMotorNo.R_LEG, 10), suppress=repeatSuppression)
        kb.add_hotkey('3+up', self._motorMove(EMotorNo.R_ANKL, 10), suppress=repeatSuppression)
        kb.add_hotkey('4+up', self._motorMove(EMotorNo.HEAD, 10), suppress=repeatSuppression)
        kb.add_hotkey('5+up', self._motorMove(EMotorNo.L_ANKL, 10), suppress=repeatSuppression)
        kb.add_hotkey('6+up', self._motorMove(EMotorNo.L_LEG, 10), suppress=repeatSuppression)
        kb.add_hotkey('7+up', self._motorMove(EMotorNo.L_ARM, 10), suppress=repeatSuppression)
        kb.add_hotkey('1+down', self._motorMove(EMotorNo.R_ARM, -10), suppress=repeatSuppression)
        kb.add_hotkey('2+down', self._motorMove(EMotorNo.R_LEG, -10), suppress=repeatSuppression)
        kb.add_hotkey('3+down', self._motorMove(EMotorNo.R_ANKL, -10), suppress=repeatSuppression)
        kb.add_hotkey('4+down', self._motorMove(EMotorNo.HEAD, -10), suppress=repeatSuppression)
        kb.add_hotkey('5+down', self._motorMove(EMotorNo.L_ANKL, -10), suppress=repeatSuppression)
        kb.add_hotkey('6+down', self._motorMove(EMotorNo.L_LEG, -10), suppress=repeatSuppression)
        kb.add_hotkey('7+down', self._motorMove(EMotorNo.L_ARM, -10), suppress=repeatSuppression)
        kb.add_hotkey('ctrl+1+up', self._motorMove(EMotorNo.R_ARM, 5), suppress=repeatSuppression)
        kb.add_hotkey('ctrl+2+up', self._motorMove(EMotorNo.R_LEG, 5), suppress=repeatSuppression)
        kb.add_hotkey('ctrl+3+up', self._motorMove(EMotorNo.R_ANKL, 5), suppress=repeatSuppression)
        kb.add_hotkey('ctrl+4+up', self._motorMove(EMotorNo.HEAD, 5), suppress=repeatSuppression)
        kb.add_hotkey('ctrl+5+up', self._motorMove(EMotorNo.L_ANKL, 5), suppress=repeatSuppression)
        kb.add_hotkey('ctrl+6+up', self._motorMove(EMotorNo.L_LEG, 5), suppress=repeatSuppression)
        kb.add_hotkey('ctrl+7+up', self._motorMove(EMotorNo.L_ARM, 5), suppress=repeatSuppression)
        kb.add_hotkey('ctrl+1+down', self._motorMove(EMotorNo.R_ARM, -5), suppress=repeatSuppression)
        kb.add_hotkey('ctrl+2+down', self._motorMove(EMotorNo.R_LEG, -5), suppress=repeatSuppression)
        kb.add_hotkey('ctrl+3+down', self._motorMove(EMotorNo.R_ANKL, -5), suppress=repeatSuppression)
        kb.add_hotkey('ctrl+4+down', self._motorMove(EMotorNo.HEAD, -5), suppress=repeatSuppression)
        kb.add_hotkey('ctrl+5+down', self._motorMove(EMotorNo.L_ANKL, -5), suppress=repeatSuppression)
        kb.add_hotkey('ctrl+6+down', self._motorMove(EMotorNo.L_LEG, -5), suppress=repeatSuppression)
        kb.add_hotkey('ctrl+7+down', self._motorMove(EMotorNo.L_ARM, -5), suppress=repeatSuppression)
        kb.add_hotkey('s', self._poseStanding, suppress=repeatSuppression)
        kb.add_hotkey('m', self._poseMaeNarae, suppress=repeatSuppression)
        kb.add_hotkey('r+f', self.qumcum.RightFootStanding, suppress=repeatSuppression)
        kb.add_hotkey('l+f', self.qumcum.LeftFootStanding, suppress=repeatSuppression)
        kb.add_hotkey('w', self.qumcum.Walk, suppress=repeatSuppression)
        kb.add_hotkey('ctrl+w', self.qumcum.WalkStop, suppress=repeatSuppression)
        kb.add_hotkey('b', self.qumcum.BackWalk, suppress=repeatSuppression)
        kb.add_hotkey('l+t', self.qumcum.TurnLeft, suppress=repeatSuppression)
        kb.add_hotkey('r+t', self.qumcum.TurnRight, suppress=repeatSuppression)
        kb.add_hotkey('h', self._showKeyGuide, suppress=repeatSuppression)
        kb.add_hotkey('c', self._getCurrentCaribOffset, suppress=repeatSuppression)
        kb.add_hotkey('p', self._getCurrentPose, suppress=repeatSuppression)
        self._showKeyGuide()
        kb.wait('escape')
    
    def Exit(self) -> None:
        super().Exit()
        kb.clear_all_hotkeys()

    def _showKeyGuide(self) -> None:
        print('----- Adjust Motor Mode -----')
        print('[1 + arrow_up/down + (ctrl)]:     Right Arm   +/-10 (ctrl:+/-5) +上/-下')
        print('[2 + arrow_up/down + (ctrl)]:     Right Leg   +/-10 (ctrl:+/-5) +外回り/-内回り')
        print('[3 + arrow_up/down + (ctrl)]:     Right Ankle +/-10 (ctrl:+/-5) +外向け/-内向け')
        print('[4 + arrow_up/down + (ctrl)]:     Head        +/-10 (ctrl:+/-5) +左/-右')
        print('[5 + arrow_up/down + (ctrl)]:     Left Ankle  +/-10 (ctrl:+/-5) +内向け/-外向け')
        print('[6 + arrow_up/down + (ctrl)]:     Left Leg    +/-10 (ctrl:+/-5) +内回り/-外回り')
        print('[7 + arrow_up/down + (ctrl)]:     Left Arm    +/-10 (ctrl:+/-5) +下/-上')
        print('[s]:                              Standing')
        print('[m]:                              MaeNarae')
        print('[r+f]:                            Right Foot Standing')
        print('[l+f]:                            Left Foot Standing')
        print('[w]:                              Walk')
        print('[ctrl+w]:                         Walk Stop')
        print('[b]:                              BackWalk')
        print('[l+t]:                            Turn Left')
        print('[r+t]:                            Turn Right')
        print('[c]:                              Show current carib offset')
        print('[p]:                              Show current pose')
        print('[esc]:                            Exit')

    def _motorMove(self, motorNo: EMotorNo, delta:int):
        def motorMove() -> None:
            self.qumcum.motorSeq.RotateAdd(motorNo, delta, 300)
        return motorMove
    
    def _poseStanding(self):
        self.qumcum.Standing()
    
    def _poseMaeNarae(self):
        self.qumcum.MaeNarae()
    
    def _getCurrentCaribOffset(self):
        carib : dict[EMotorNo, int] = self.qumcum.motorSeq.GetCaribOffset()
        print('----- Carib Offset -----')
        for motor, value in carib.items():
            print(f'{motor.name}: {value}')
    
    def _getCurrentPose(self):
        pose : dict[EMotorNo, int] = self.qumcum.motorSeq.GetCurrentPose()
        print('----- Current Pose -----')
        for motor, value in pose.items():
            print(f'{motor.name}: {value}')



class QumcumAPITestMode(InterfaceMode):
    def __init__(self, qumcum: QumcumController) -> None:
        super().__init__(qumcum)

    def Start(self) -> None:
        super().Start()
        time.sleep(1)
        sys.stdout.flush()
        while(True):
            print('----- Select API -----')
            print('[1]: get_init')
            print('[2]: get_info')
            print('[3]: get_position')
            print('[4]: get_motor_positions')
            print('[5]: get_motor_position')
            print('[6]: get_sensor_value')
            print('[q]: Exit')
            input_str = input('Enter select api: ')
            if input_str == 'q':
                break
            elif not input_str.isdecimal():
                continue
            api_no = int(input_str)
            self._runQumcumAPI(api_no)
    
    def Exit(self) -> None:
        super().Exit()
    
    def _runQumcumAPI(self, api_no:int):
        if api_no == 1:
            self._checkQumcumRes(qumcum_ble.get_init())
        elif api_no == 2:
            self._checkQumcumRes(qumcum_ble.get_info())
        elif api_no == 3:
            self._checkQumcumRes(qumcum_ble.get_position())
        elif api_no == 4:
            self._checkQumcumRes(qumcum_ble.get_motor_positions())
        elif api_no == 5:
            motor_no = input('Enter motor no: ')
            self._checkQumcumRes(qumcum_ble.get_motor_position(motor_no))
        elif api_no == 6:
            self._checkQumcumRes(qumcum_ble.get_sensor_value())
    
    def _checkQumcumRes(self, api_ret:tuple[int,str]):
        if api_ret[0] == 0:
            print(api_ret[1])
        else:
            print('Error Qumcum Response')



class KeyboardListener:
    def __init__(self, qumcum: QumcumController) -> None:
        self.qumcum = qumcum
        self.mode = InterfaceMode(self.qumcum)
        pass

    def Run(self) -> None:
        # kb.on_press(lambda e: print(f'Push Key: {e.name}'))
        while self._selectMode() != 0:
            self.mode.Start()
            time.sleep(1)

    def _selectMode(self) -> int:
        print('---- Select Mode ----')
        print('[1]  : Adjust default motor position mode')
        print('[2]  : Manual control mode')
        print('[3]  : Qumcum API TEST mode')
        print('[esc]: Exit')
        while True:
            if kb.is_pressed('1'):
                self.mode.Exit()
                self.mode = AdjustMotorMode(self.qumcum)
                return 1
            elif kb.is_pressed('2'):
                self.mode.Exit()
                self.mode = ManualControlMode(self.qumcum)
                return 2
            elif kb.is_pressed('3'):
                self.mode.Exit()
                self.mode = QumcumAPITestMode(self.qumcum)
                return 3
            elif kb.is_pressed('escape'):
                self.mode.Exit()
                return 0
                
