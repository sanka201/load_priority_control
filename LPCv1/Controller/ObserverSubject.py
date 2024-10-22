from abc import ABC, abstractmethod
import sys
sys.path.append("/home/sanka/NIRE_EMS/volttron/LoadPriorityControl/LPCv1/")
from Model.Observer import Observer

class ObserverSubject(ABC):
    """_summary_
      This interface implement the methods necessary for the subject that need to be observed.
    Args:
        ABC (_type_): _description_
    """    
    
    def __init__(self) -> None:
        super().__init__()
        
    @abstractmethod
    def register_Observer(self,obsrver: Observer)->None:
        pass
    
    @abstractmethod
    def remove_Observer(observer: Observer) -> None:
        pass
    
    @abstractmethod
    def notify_Observers(self)->None:
        pass