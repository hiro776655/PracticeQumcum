#coding: UTF-8

import keyboard as kb
import time
from KUSANAGI.qumcum_controller import QumcumController
from KUSANAGI.defines import EMotorNo

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
        kb.add_hotkey('1+up', self._motorAdjust(EMotorNo.R_ARM, 1.0))
        kb.add_hotkey('2+up', self._motorAdjust(EMotorNo.R_LEG, 1.0))
        kb.add_hotkey('3+up', self._motorAdjust(EMotorNo.R_ANKL, 1.0))
        kb.add_hotkey('4+up', self._motorAdjust(EMotorNo.HEAD, 1.0))
        kb.add_hotkey('5+up', self._motorAdjust(EMotorNo.L_ANKL, 1.0))
        kb.add_hotkey('6+up', self._motorAdjust(EMotorNo.L_LEG, 1.0))
        kb.add_hotkey('7+up', self._motorAdjust(EMotorNo.L_ARM, 1.0))
        kb.add_hotkey('1+down', self._motorAdjust(EMotorNo.R_ARM, -1.0))
        kb.add_hotkey('2+down', self._motorAdjust(EMotorNo.R_LEG, -1.0))
        kb.add_hotkey('3+down', self._motorAdjust(EMotorNo.R_ANKL, -1.0))
        kb.add_hotkey('4+down', self._motorAdjust(EMotorNo.HEAD, -1.0))
        kb.add_hotkey('5+down', self._motorAdjust(EMotorNo.L_ANKL, -1.0))
        kb.add_hotkey('6+down', self._motorAdjust(EMotorNo.L_LEG, -1.0))
        kb.add_hotkey('7+down', self._motorAdjust(EMotorNo.L_ARM, -1.0))
        kb.add_hotkey('ctrl+1+up', self._motorAdjust(EMotorNo.R_ARM, 0.1))
        kb.add_hotkey('ctrl+1+down', self._motorAdjust(EMotorNo.R_ARM, -0.1))
        kb.add_hotkey('h', self._showKeyGuide)
        kb.add_hotkey('a', self._autoAdjust)
        kb.add_hotkey('p', self._getCurrentAdjustValue)
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
        print('[5 + arrow_up/down]:     Left Arm    +/-1')
        print('[6 + arrow_up/down]:     Left Leg    +/-1')
        print('[7 + arrow_up/down]:     Left Ankle  +/-1')
        print('[a]:                     Auto Adjust Full body')
        print('[p]:                     Show current adjust value')
        print('[esc]:                   Exit')
        # print('[1 + arrow_up/down + ctrl]: Right Arm +/-0.1')

    def _motorAdjust(self, motorNo: EMotorNo, delta:float):
        def motorAdjust() -> None:
            self.qumcum.motorSeq.Adjust(motorNo, delta)
        return motorAdjust

    def _autoAdjust(self):
        return self.qumcum.AdjustDefaltPosition
    
    def _getCurrentAdjustValue(self):
        pos : dict[EMotorNo, float] = self.qumcum.motorSeq.GetCurrentPos()
        for motor, value in pos.items():
            print(f'{motor.name}: {value}')



class ManualControlMode(InterfaceMode):
    def __init__(self, qumcum: QumcumController) -> None:
        super().__init__(qumcum)

    def Start(self) -> None:
        super().Start()
        kb.add_hotkey('1+up', self._motorMove(EMotorNo.R_ARM, 10.0))
        kb.add_hotkey('2+up', self._motorMove(EMotorNo.R_LEG, 10.0))
        kb.add_hotkey('3+up', self._motorMove(EMotorNo.R_ANKL, 10.0))
        kb.add_hotkey('4+up', self._motorMove(EMotorNo.HEAD, 10.0))
        kb.add_hotkey('5+up', self._motorMove(EMotorNo.L_ANKL, 10.0))
        kb.add_hotkey('6+up', self._motorMove(EMotorNo.L_LEG, 10.0))
        kb.add_hotkey('7+up', self._motorMove(EMotorNo.L_ARM, 10.0))
        kb.add_hotkey('1+down', self._motorMove(EMotorNo.R_ARM, -10.0))
        kb.add_hotkey('2+down', self._motorMove(EMotorNo.R_LEG, -10.0))
        kb.add_hotkey('3+down', self._motorMove(EMotorNo.R_ANKL, -10.0))
        kb.add_hotkey('4+down', self._motorMove(EMotorNo.HEAD, -10.0))
        kb.add_hotkey('5+down', self._motorMove(EMotorNo.L_ANKL, -10.0))
        kb.add_hotkey('6+down', self._motorMove(EMotorNo.L_LEG, -10.0))
        kb.add_hotkey('7+down', self._motorMove(EMotorNo.L_ARM, -10.0))
        kb.add_hotkey('ctrl+1+up', self._motorMove(EMotorNo.R_ARM, 5.0))
        kb.add_hotkey('ctrl+2+up', self._motorMove(EMotorNo.R_LEG, 5.0))
        kb.add_hotkey('ctrl+3+up', self._motorMove(EMotorNo.R_ANKL, 5.0))
        kb.add_hotkey('ctrl+4+up', self._motorMove(EMotorNo.HEAD, 5.0))
        kb.add_hotkey('ctrl+5+up', self._motorMove(EMotorNo.L_ANKL, 5.0))
        kb.add_hotkey('ctrl+6+up', self._motorMove(EMotorNo.L_LEG, 5.0))
        kb.add_hotkey('ctrl+7+up', self._motorMove(EMotorNo.L_ARM, 5.0))
        kb.add_hotkey('ctrl+1+down', self._motorMove(EMotorNo.R_ARM, -5.0))
        kb.add_hotkey('ctrl+2+down', self._motorMove(EMotorNo.R_LEG, -5.0))
        kb.add_hotkey('ctrl+3+down', self._motorMove(EMotorNo.R_ANKL, -5.0))
        kb.add_hotkey('ctrl+4+down', self._motorMove(EMotorNo.HEAD, -5.0))
        kb.add_hotkey('ctrl+5+down', self._motorMove(EMotorNo.L_ANKL, -5.0))
        kb.add_hotkey('ctrl+6+down', self._motorMove(EMotorNo.L_LEG, -5.0))
        kb.add_hotkey('ctrl+7+down', self._motorMove(EMotorNo.L_ARM, -5.0))
        kb.add_hotkey('h', self._showKeyGuide)
        kb.add_hotkey('p', self._getCurrentAdjustValue)
        self._showKeyGuide()
        kb.wait('escape')
    
    def Exit(self) -> None:
        super().Exit()
        kb.clear_all_hotkeys()

    def _showKeyGuide(self) -> None:
        print('----- Adjust Motor Mode -----')
        print('[1 + arrow_up/down + (ctrl)]:     Right Arm   +/-10 (ctrl:+/-5)')
        print('[2 + arrow_up/down + (ctrl)]:     Right Leg   +/-10 (ctrl:+/-5)')
        print('[3 + arrow_up/down + (ctrl)]:     Right Ankle +/-10 (ctrl:+/-5)')
        print('[4 + arrow_up/down + (ctrl)]:     Head        +/-10 (ctrl:+/-5)')
        print('[5 + arrow_up/down + (ctrl)]:     Left Arm    +/-10 (ctrl:+/-5)')
        print('[6 + arrow_up/down + (ctrl)]:     Left Leg    +/-10 (ctrl:+/-5)')
        print('[7 + arrow_up/down + (ctrl)]:     Left Ankle  +/-10 (ctrl:+/-5)')
        print('[esc]:                            Exit')

    def _motorMove(self, motorNo: EMotorNo, delta:float):
        def motorMove() -> None:
            self.qumcum.motorSeq.RoateAdd(motorNo, delta, 300)
        return motorMove
    
    def _getCurrentAdjustValue(self):
        def getCurrentAdjustValue() -> None:
            pos : dict[EMotorNo, float] = self.qumcum.motorSeq.GetCurrentPos()
            for motor, value in pos.items():
                print(f'{motor.name}: {value}')
        return getCurrentAdjustValue



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
            elif kb.is_pressed('escape'):
                self.mode.Exit()
                return 0
                
