import sys
sys.path.append("/home/sanka/NIRE_EMS/volttron/LoadPriorityControl/LPCv1/")
from Model.Observer import Observer
from Model.IoTDevice import IoTDevice
from Model.IoTMessage import IoTMessage
from View.Send import Send
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class EVCharger(IoTDevice,Observer):
    """_summary_
    EvChager present the object for Juice Box chager 
    Args:
        IoTDevice (_type_): _description_
        Observer (_type_): _description_
    """
    
    def __init__(self, id:str, vip) -> None:
        super().__init__()
        """_summary_

        Args:
            id (int): device Id
            vip (obj): volttron vip connection for communication in the volttron message bus
        """  
        self._id=id
        self._status=0
        self._power_consumption=0
        self._current=0
        self._voltage=0
        self._frequency=0
        self._currentcommand=0
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
        self._deviceType='EV'
        self._is_defferable= True
        self._can_control_power=True
        self._energy_consumption=0
        self._temperature=0
        self._power_consumption_before_last_command=0
        
    def turn_On(self) -> None:
        self._message.message_type='command'
        self._message.payload={'cmd':40}
        self._message.priority=self._priority
        self.publish()
        self._last_command=self._message
        self._status=1
        logger.info(">>>>>>>>>>>>>>>>>>>>>> Turning on EV charger")
    
    def turn_Off(self) -> None:
        self._message.message_type='command'
        self._message.payload={'cmd':0}
        self._message.priority=self._priority
        self.publish()
        self._last_command=self._message
        self._status=0
        logger.info(">>>>>>>>>>>>>>>>>>>>>> Turning of EV charger")
    
    def set_parameters(self,para: int) -> None:
        self._message.message_type='command'
        self._message.payload={'cmd':para}
        self._message.priority=self._priority
        self.publish()
        self._last_command=self._message
        logger.info(">>>>>>>>>>>>>>>>>>>>>> Changing Power of the EV")
    
    def set_Power_Consumption(self, power: int) -> None:
        self._power_consumption = power
    
    def get_Power_Consumption(self) -> int:
        return super().get_Power_Consumption()
    
    def get_Device_Id(self) -> int:
        return super().get_Device_Id()
    
    def set_Priority(self, priority: int) -> None:
        return super().set_Priority(priority)
    
    def get_Priority(self) -> int:
        return super().get_Priority()
    
    def update(self, current: int, frequency: int, priority: int, voltage: float, powercommand :int, energyconsumption: int, temperature: int, status: int) -> None:

        self.set_Power_Consumption(voltage*current/100)
        self._current=current
        self._voltage=voltage
        self._frequency=frequency
        self._currentcommand=powercommand
        self._priority=priority
        self._energy_consumption=energyconsumption
        self._status= status
        self._temperature=temperature
        if  self._power_consumption > self._max_power_rating:
            self._max_power_rating= self._power_consumption
        logger.info(f"updating the EV charger{ self._id}: power {self._power_consumption} : priority { self._priority} : status {self._status}: powr_multiply_factor {self._power_multiply_factor}")

    def publish(self) -> bool:
        """_summary_
        this method publish the message to the volttron message bus
        Returns:
            bool: state of sending data
        """        
        self._send.publish(self._message,self._deviceType)
        return bool