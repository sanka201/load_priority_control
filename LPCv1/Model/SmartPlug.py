import sys
sys.path.append("/home/sanka/NIRE_EMS/volttron/LoadPriorityControl/LPCv1/")
from Model.Observer import Observer
from Model.IoTDevice import IoTDevice
from Model.IoTMessage import IoTMessage
from View.Send import Send
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class SmartPlug(Observer,IoTDevice):
    """_summary_
    The smart plug describes the methods to control and monitor a smart Plug
    Args:
        Observer ( Interface): observer for updating IoTdevice statusS
        IoTDevice ( Interface): Interface to use to derive the SmartPlug class
    """    
    def __init__(self,id :str,vip) -> None:
        """_summary_

        Args:
            id (int): device Id
            vip (obj): volttron vip connection for communication in the volttron message bus
        """        
        super().__init__()
        self._id=id
        self._status=0
        self._power_consumption=0
        self._current=0
        self._voltage=0
        self._frequency=0
        self._connected=0
        self._flagged=False
        self._last_command=0
        self._priority=0
        self._vip=vip
        self._send=Send(vip)
        self._message= IoTMessage(device_id=id,message_type=None,payload=['command',None],timestamp=datetime.now())
        self._observerid=id
        self._max_power_rating=0
        self._power_multiply_factor=1
        self._control_attempts=0
        self._deviceType='plug'
        self._is_defferable= False
        self._can_control_power= False
        self._energy_consumption=0
        self._temperature=0
        
    def turn_On(self) -> None:
        self._message.message_type='command'
        self._message.payload={'cmd':1}
        self._message.priority=self._priority
        self.publish()
        self._last_command=self._message
        
    def turn_Off(self) -> None:
        self._message.message_type='command'
        self._message.payload={'cmd':0}
        self._message.priority=self._priority
        self.publish()
        self._last_command=self._message
    
    def get_Power_Consumption(self) -> int:
        return self._power_consumption
    
    def set_Power_Consumption(self, power: int) -> None:
        self._power_consumption = power*self._power_multiply_factor
    
    def get_Device_Id(self) -> int:
        return self._id
    
    def set_Priority(self, priority: int) -> None:
        self._priority=priority
    
    def get_Priority(self) -> int:
        return self._priority
    
    def update(self, power_consumption: int, status: int, priority: int) -> None:
        """_summary_
        this method is executed by the observer when ever the power consumption is updated
        Args:
            power_consumption (int): instatntanious power consumption of the smart plug
        """        
        self.set_Power_Consumption(power_consumption)
        self._priority=priority
        self._status=status
        if  self._power_consumption > self._max_power_rating:
            self._max_power_rating= self._power_consumption
        logger.info(f"updating the smart plug{ self._id}: power {power_consumption} : priority { self._priority} : status {self._status}: powr_multiply_factor {self._power_multiply_factor}: max_power {self._max_power_rating}")
        
    def _check_Health(self)-> None:
        pass
    
    def isFlaged(self)->None:
        return self._flagged == True
    
    def publish(self) -> bool:
        """_summary_
        this method publish the message to the volttron message bus
        Returns:
            bool: state of sending data
        """        
        self._send.publish(self._message,self._deviceType)
        return bool
    
    def set_parameters(self, para : int)->None:
        pass
    
# if __name__ == "__main__":
    
#     plug = SmartPlug(1,1)
#     plug.turn_On()
#     plug.turn_Off()
#     print(plug.isFlaged())