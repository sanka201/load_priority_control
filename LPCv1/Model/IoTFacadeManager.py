from abc import ABC, abstractmethod
import sys
sys.path.append("/home/sanka/NIRE_EMS/volttron/LoadPriorityControl/LPCv1/")
from Model.IoTDeviceGroup import IoTDeviceGroup
class IoTFacadeManager(ABC):
    
    def __init__(self) -> None:
        super().__init__()
        self._groups={}
        
    @abstractmethod
    def group_By_Priority(self,key)->IoTDeviceGroup:
        pass
    
    @abstractmethod
    def clear_Groups_Stratgies(self)->None:
        pass
    
    @abstractmethod
    def add_Group(self,group:IoTDeviceGroup)->None:
        pass
    
    @abstractmethod
    def remove_Group(self,group: IoTDeviceGroup)->None:
        pass
    
    @abstractmethod
    def execute_Strategy(self)->None:
        pass 
    
    @abstractmethod
    def set_Group_Stratagy(self,group,controller)-> None:
        pass