from abc import ABC, abstractmethod

class IoTDevice(ABC):
    
    def __init__(self) -> None:
        super().__init__()
    
    @abstractmethod
    def turn_On(self)->None:
        pass
    
    @abstractmethod
    def turn_Off(self)->None:
        pass
    
    @abstractmethod
    def get_Power_Consumption(self)->int:
        pass
    
    @abstractmethod
    def set_Power_Consumption(self,power:int)->None:
        pass
    
    @abstractmethod
    def get_Device_Id(self)->int:
        pass
    
    @abstractmethod
    def set_Priority(self, priority :int) -> None:
        pass
    
    @abstractmethod
    def get_Priority(self) -> int:
        pass
    
    @abstractmethod
    def set_parameters(self, para: int)->None:
        pass