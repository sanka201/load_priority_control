from abc import ABC, abstractmethod

class Observer(ABC):
    
    def __init__(self) -> None:
        super().__init__()
        self._observerid=None
        
    @abstractmethod    
    def update(self,power_consumption :int, status: int, priority: int, power_multiply_factor: float) -> None:
        pass