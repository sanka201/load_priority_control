
import sys
sys.path.append("/home/sanka/NIRE_EMS/volttron/LoadPriorityControl/LPCv1/")
from Model.IoTFacade import IoTFacade
from Model.IoTDevice import IoTDevice
from Model.SmartPlug import SmartPlug
import logging
from itertools import groupby
logger = logging.getLogger(__name__)


class IoTDeviceGroup(IoTFacade):
    """_summary_
    This class extend the IoTFacade interface to implements the methods to manage and control group of IoT devices
    Args:
        IoTFacade (_type_): _description_
    """    
    def __init__(self) -> None:
        super().__init__()
        self._devices={}
        
    def turn_On(self, device_id: int) -> None:
        if bool(self._devices):
            print("turn_On")
            self._devices[device_id].turn_On()
        else:
            try:
                raise ValueError("the facade is empty: did you add devices to facade ?")
            except ValueError as e:
                logger.error(f"Error in IoTDevice group turnon method: {e}")
    
    def turn_Off(self, device_id: int) -> None:
        if bool(self._devices):
            print("turn_Off")
            self._devices[device_id].turn_Off()
        else:
            try:
                raise ValueError("the facade is empty: did you add devices to facade ?")
            except ValueError as e:
                logger.error(f"Error in IoTDevice group turnon method: {e}")
    
    def get_Power_Consumption(self, device_id: int) -> int:
        return self._devices[device_id].get_Power_Consumption()
    
    def set_Priority(self, device_id: int, priority: int) -> None:
        self._devices[device_id].set_Priority(priority)
        
    def get_Priority(self, device_id: int) -> int:
        return self._devices[device_id].set_Priority()
    
    def add_Device(self, device: IoTDevice) -> None:
        self._devices[device._id]=device
    
    def remove_Device(self, device: IoTDevice) -> None:
        try:
            if self._devices:
                del self._devices[device._id]
            else:
                try:
                    raise ValueError("Facade is Empty")
                except ValueError as e:
                    logger.error(f"Facade is Empty {e}")
        except Exception as e:
                logger.error(f"Error in the Facade: {e}")
    
    def get_Devices(self) -> dict:
        return self._devices
    
    def all_On(self) -> None:
        for device in self._devices:
            self.turn_On(device._id)
    
    def all_Off(self) -> None:
        for device in self._devices:
            self.turn_On(device._id)
            
    def get_Facade_Consumption(self)->dict:
        sorted_smart_plugs = sorted(self._devices.values(),key=lambda plug: plug._priority)
        power_consumption_by_priority = {}
        for key, group in groupby(sorted_smart_plugs, key=lambda plug: plug._priority):
            power_consumption_by_priority[key] = sum(plug._power_consumption for plug in group)
        return power_consumption_by_priority
    
    def get_Facade_Max_rating(self)->dict:
        sorted_smart_plugs = sorted(self._devices.values(),key=lambda plug: plug._priority)
        max_power_rating_by_priority = {}
        for key, group in groupby(sorted_smart_plugs, key=lambda plug: plug._priority):
            max_power_rating_by_priority[key] = sum(plug._max_power_rating for plug in group)
        return max_power_rating_by_priority
    
    def get_Facade_Max_rating_for_on_loads(self)->dict:
        sorted_smart_plugs = sorted(self._devices.values(),key=lambda plug: plug._status)
        turned_on_loads=sum([0 if device._status == 0 else device._max_power_rating for device in self._devices.values()])
        tuned_off_loads=turned_on_loads-sum([ device._max_power_rating for device in self._devices.values()])
        return turned_on_loads, abs(tuned_off_loads)
        
    def set_parameters(self_id: int)->None: # this is to set the additional parameters of a device
        pass
        
#if __name__ == "__main__":
        # plug1 =SmartPlug(1,1)
        # plug2 =SmartPlug(2,1)
        # plug3 =SmartPlug(3,1)
        
        # plug1.set_Power_Consumption(100)
        # plug2.set_Power_Consumption(30)
        # plug3.set_Power_Consumption(200)
        # plug1.set_Priority(2)
        # plug2.set_Priority(0)
        # plug3.set_Priority(0)
        
        # group = IoTDeviceGroup()
        # group.add_Device(plug1)
        # group.add_Device(plug2)
        # group.add_Device(plug3)
        # print(group.get_Facade_Consumption())
        