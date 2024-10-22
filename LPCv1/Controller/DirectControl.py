import sys
sys.path.append("/home/sanka/NIRE_EMS/volttron/LoadPriorityControl/LPCv1/")
from Model.IoTDeviceGroup import IoTDeviceGroup
from Controller.ControlStrategy import ControlStrategy
import logging

logger = logging.getLogger(__name__)

class DirectControl(ControlStrategy):
    
    def __init__(self) -> None:
        super().__init__()
        self._controlType='direct'
        
    def execute(self,group: IoTDeviceGroup,cmd: any) -> None:
        for device in cmd:
            if cmd[device]==1:
                group.turn_On(device)
            elif cmd[device]==0:
                group.turn_Off(device)
            else:
                try:
                    raise ValueError('Command is not compatible')
                except Exception as e:
                    logger.error(f"Command is not compatible {e}")