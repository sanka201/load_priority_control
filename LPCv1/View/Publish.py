from abc import ABC, abstractmethod


class Publish(ABC):
    
    def __init__(self) -> None:
        super().__init__()
    
    @abstractmethod
    def publish(self,message:dict)->bool:
        pass