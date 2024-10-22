import sys
sys.path.append("/home/sanka/NIRE_EMS/volttron/LoadPriorityControl/LPCv1/")
from Model.IoTDeviceGroup import IoTDeviceGroup
from Controller.ControlStrategy import ControlStrategy
import logging

logger = logging.getLogger(__name__)

class IncrementalControl(ControlStrategy):
    
    def __init__(self) -> None:
        super().__init__()
        self._controlType='increment'
        
    def execute(self,group: IoTDeviceGroup, cmd: any) -> None:
        print("executing Incremntal control")