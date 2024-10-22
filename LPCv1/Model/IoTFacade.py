from abc import ABC, abstractmethod
import sys
sys.path.append("/home/sanka/NIRE_EMS/volttron/LoadPriorityControl/LPCv1/")
from Model.IoTDevice import IoTDevice


class IoTFacade(ABC):
    def __init__(self) -> None:
        super().__init__()
        """_summary_
        The IoTFacade interface defines the methods for managing group of Smart devices
        """    
        
    @abstractmethod
    def turn_On(self, device_id: int)->None:
        pass
    
    @abstractmethod
    def set_parameters(self_id: int)->None: # this is to set the additional parameters of a device
        pass
    
    @abstractmethod
    def turn_Off(self,device_id: int)-> None:
        pass
    
    @abstractmethod
    def add_Device(self, device: IoTDevice)->None:
        pass
    
    @abstractmethod
    def remove_Device(self, device: IoTDevice)->None:
        pass
    
    @abstractmethod
    def get_Power_Consumption(self, device_id: int) ->int:
        pass
    
    @abstractmethod
    def get_Facade_Consumption(self)->dict:
        pass
    @abstractmethod   
    def get_Facade_Max_rating(self)->dict:
        pass
    
    @abstractmethod
    def set_Priority(self, device_id: int, priority: int) -> None:
        pass
    
    @abstractmethod 
    def get_Priority(self,device_id: int) ->int:
        pass
    
    @abstractmethod
    def get_Devices(self)->dict:
        pass
    
    @abstractmethod
    def all_On(self)->None:
        pass
    
    @abstractmethod
    def all_Off(self)->None:
        pass
        