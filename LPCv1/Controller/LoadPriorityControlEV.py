import sys
sys.path.append("/home/sanka/NIRE_EMS/volttron/LoadPriorityControl/LPCv1/")
from Model.IoTDeviceGroup import IoTDeviceGroup
from Controller.ControlStrategy import ControlStrategy
import logging
from itertools import groupby
from time import sleep

logger = logging.getLogger(__name__)

class LoadPriorityControlEV(ControlStrategy):
    def __init__(self) -> None:
        super().__init__()
        self._controlType='lpc'
        self.priority_groups = {}
                
    def _group_by_Priorities(self, group,_reverse=False):
        sorted_groups={}
        sorted_smart_plugs = sorted(group._devices.values(),key=lambda plug: plug._priority,reverse=_reverse)
        for key, sortedgroup in groupby(sorted_smart_plugs, key=lambda plug: plug._priority):
                sorted_groups[key] = list(sortedgroup)
        return  sorted_groups
        
    def execute(self, group: IoTDeviceGroup, cmd: any) -> None:
        total_consumption = sum(group.get_Facade_Consumption().values())
        on_loads,off_loads=group.get_Facade_Max_rating_for_on_loads()

        logger.info(f"Haioooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo >>>>>>>>>>>>>>>>>>>>>>>>>>>> total consumption {total_consumption}, { self._group_by_Priorities(group)} . >>>>>>>>>>>>>>>>>>>>>>> {cmd}")
        decoded_cmd=cmd[1]
        ## Shedding control section 
        if total_consumption > decoded_cmd:
             logger.info("Threshold exceeded. Turning off devices...")
             priority_groups=self._group_by_Priorities(group,False)
             for priority in priority_groups.keys():
                for device in priority_groups[priority] :
                    logger.info(f"Threshold exceeded. Turning off devices...{device._power_consumption}.. ID {device._id}")
                    if total_consumption > decoded_cmd and device._status !=11:
                        if device._can_control_power==True and device._status==0:
                            pass
                        if device._can_control_power==True and device._status==1:
                                device._power_consumption_before_last_command=device._power_consumption
                                device.turn_Off()
                                device._last_command=0
                                device._flagged=False
                                logger.info(f"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ Turning off device {device._id} with priority {priority}, and total  consumption {total_consumption}")
                        if device._can_control_power==True and device._status==2:
                            abserror=abs(total_consumption-decoded_cmd)
                            if device._power_consumption > abserror:
                                para= int((device._power_consumption-abserror)/device._voltage*10)
                                device.set_parameters(round(para))
                                device._last_command=0
                                device._flagged=False
                                total_consumption -= abserror 
                                device._power_consumption_before_last_command=device._power_consumption
                                logger.info(f"PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP Setting varible power value {device._id} , total on loads {on_loads} with priority {priority}, and total  consumption {abserror} and control command {para}PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
                            else:
                                device.turn_Off()
                                device._power_consumption_before_last_command=device._power_consumption
                                device._last_command=0
                                device._flagged=False
                                logger.info(f"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ Turning off device {device._id} with priority {priority}, , total on loads {on_loads} and total  consumption {total_consumption}")
                            
                        elif device._can_control_power==False:
                            device.turn_Off()
                            device._last_command=0
                            device._flagged=False
                            if device._last_command==0:
                                    device._control_attempts+=1
                            sleep(.25)
                            logger.info(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Turning off device {device._id} with priority {priority},  , total on loads {on_loads} and total  consumption {total_consumption}")
                            total_consumption -= device._power_consumption 
                        else:
                            pass      
                    elif device._status ==11:
                        device._flagged=True
                    else:
                        break
                                  
        ## Incremental control section 
        elif total_consumption < decoded_cmd:

             priority_groups=self._group_by_Priorities(group,True)
             max_rating=sum(group. get_Facade_Max_rating().values())
             for priority in priority_groups.keys():
                 for device in priority_groups[priority]:
                     
                     if device._can_control_power:
                        
                        logger.info(f"Below threshold. Turning on devices ........{device._id} , status {device._status}, last command {device._last_command}, total consumption {total_consumption}, total on loads {on_loads} >>>>>>>>>>>>>>>>>>>>>>>>")
                        if (total_consumption < decoded_cmd and device._last_command==0) and device._status !=11:
                            abserror=abs(total_consumption-decoded_cmd)
                            para= int((device._power_consumption+abserror)/device._voltage*10)-2
                            if para <0:
                                para=0
                            if para >40:
                                device.set_parameters(40)
                                device.turn_On()
                                device._last_command=1
                                logger.info(f"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ Setting varible power value on device {device._id} with priority {priority}, and total  c")
                                on_loads += device._max_power_rating
                            else:
                                logger.info(f"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ Setting varible power value on device {device._id} with priority {priority}, and total  consumption {total_consumption}, , total on loads {on_loads} and parameter {para} abserrot{abserror}")
                                device.set_parameters(para)
                                on_loads += para*device._voltage/10
                                device._last_command=0
                            device._flagged=True
                            sleep(.25)

                            
                        elif  device._last_command==1:
                            total_consumption -= device._max_power_rating
                        elif  device._status ==11:
                            device._flagged=True
                            total_consumption -= device._max_power_rating                         
                        else:
                            break

                     else:
                        on_loads += device._max_power_rating
                        logger.info(f"Below threshold. Turning on devices ........{device._id} , status {device._status}, last command {device._last_command}, total consumption {total_consumption}, , total on loads {on_loads}, decoded comand {decoded_cmd} >>>>>>>>>>>>>>>>>>>>>>>>")
                        if (on_loads < decoded_cmd and device._last_command==0) and device._status !=11:
                            device.turn_On()
                            device._last_command=1
                            device._flagged=True
                            sleep(.25)
                            logger.info(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Turning on device {device._id} with priority {priority}, , total on loads {on_loads} and total  consumption {total_consumption}")
                    
                        elif  device._last_command==1:
                            on_loads -= device._max_power_rating
                        elif  device._status ==11:
                            device._flagged=True
                            on_loads -= device._max_power_rating                         
                        else:
                            print("breaking. 1st....................",)
                            break
                 if on_loads >= decoded_cmd:
                    print("breaking.....................")
                    break
