import sys
sys.path.append("/home/sanka/NIRE_EMS/volttron/LoadPriorityControl/LPCv1/")
from Controller.ControlStrategy import ControlStrategy
import logging

logger = logging.getLogger(__name__)

class SimpleControlStrategy(ControlStrategy):
    def __init__(self) -> None:
        super().__init__()
        self._controlType='simple'
        
    def execute(self,Group,cmd) -> None:
        for device_id in Group._devices.keys():
            try:
                power = Group.get_Power_Consumption(device_id)
                if power > cmd:
                    Group.turn_Off(device_id)
                else:
                    Group.turn_On(device_id)
            except ValueError as e:
                print(e)
    