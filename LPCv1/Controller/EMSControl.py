import sys
sys.path.append("/home/sanka/NIRE_EMS/volttron/LoadPriorityControl/LPCv1/")
from Controller.ControlStrategy import ControlStrategy
from Model.IoTFacade import IoTFacade
import logging

logger = logging.getLogger(__name__)
class EMSControl:
    
    def __init__(self) -> None:
        self._controlstratagey=None
        self._devicegroup=None
        self._cmd={}
        
    def execute_Strategy(self)->None:
        if not self._devicegroup:
            logger.error(f"The device group is empty")
            raise KeyError(f"The device group is empty")
        else:
            if not self._controlstratagey:
                logger.error(f"did you add the control stratagy ?")
                raise KeyError(f"did you add the control stratagy ?")
            else:
                try:
                    self._controlstratagey.execute(self._devicegroup,self._cmd)
                except Exception as e:
                    logger.error(f"error occured {e}")
                    raise KeyError(f"error occureds {e}")
        
    def set_Group(self,Group: IoTFacade) -> None:
        self._devicegroup=Group
    
    def set_Controller(self,controller,cmd)->None:
        self._controlstratagey=controller
        self._cmd=cmd
    def remove_Group(self,Group: IoTFacade)->None:
        pass
    
    
    # def add_Controller(self,controlstrategy:ControlStrategy) -> None:

    #         if controlstrategy._controlType  in self._controlstratagey:
    #             self._controlstratagey[controlstrategy._controlType].append(controlstrategy)
    #         else:
    #             self._controlstratagey[controlstrategy._controlType]=[]
    #             self._controlstratagey[controlstrategy._controlType].append(controlstrategy)

    # def remove_Controller(self,controlstrategy:ControlStrategy)->None:
    #     if  self._controlstratagey:
    #         try:
    #             self._controlstratagey[controlstrategy._controlType].remove(controlstrategy)
    #         except Exception as e:
    #             logger.error(f"error in remove controller {e}")
    #     else:
    #         pass