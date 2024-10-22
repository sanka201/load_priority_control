import sys
sys.path.append("/home/sanka/NIRE_EMS/volttron/LoadPriorityControl/LPCv1/")

from Model.IoTDeviceGroup import IoTDeviceGroup
from Model.FacadeRepository import FacadeRepository
import logging

logger = logging.getLogger(__name__)

class GroupRepository(FacadeRepository):
    
    def __init__(self, vip,agentid) -> None:
        super().__init__()
        self._vip=vip
        self._agentid=agentid
        
    def add_Facade(self, facade: IoTDeviceGroup) -> None:
        return super().add_Facade(facade)
    
    def remove_facade(sef, facade: IoTDeviceGroup) -> None:
        return super().remove_facade(facade)
    
    def update_Facade(self, message) -> None:
        result = self._vip.pubsub.publish(peer='pubsub',topic= 'record/'+str(self._agentid)+'/NIREEMS/data', message=message) 
    
    def get_Facade(self, facade: IoTDeviceGroup) -> None:
        return super().get_Facade(facade)