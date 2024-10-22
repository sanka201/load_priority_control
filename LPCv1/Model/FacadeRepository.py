from abc import ABC, abstractmethod

class FacadeRepository(ABC):
    def __init__(self) -> None:
        super().__init__()
        
    @abstractmethod
    def add_Facade(self,facade)-> None:
        pass
    
    @abstractmethod
    def get_Facade(self,facade)-> None:
        pass

    @abstractmethod
    def update_Facade(self, facade)-> None:
        pass
    
    @abstractmethod
    def remove_facade(sef, facade)->None:
        pass 