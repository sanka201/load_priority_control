
import sys
sys.path.append("/home/sanka/NIRE_EMS/volttron/LoadPriorityControl/LPCv1/")
from Controller.ObserverSubject import ObserverSubject
from Model.Observer import Observer
from Model.IoTMessage import IoTMessage
from Model.SmartPlug import SmartPlug
from Controller.EMSControl import EMSControl
import logging

logger = logging.getLogger(__name__)

class DeviceMonitor(ObserverSubject):
    
    def __init__(self) -> None:
        super().__init__()
        self._message=None
        self._observers={}
        self._notificationObserverID=None
        self._emscontroller= None
        
    def register_Observer(self,observer: Observer) -> None:
        self._observers[observer._observerid]=observer
    
    def remove_Observer(self, observer: Observer) -> None:
        try:
            if self._observers:
                del self._observers[observer._observerid]
            else:
                try:
                    raise ValueError("Observers are Empty")
                except ValueError as e:
                    logger.error(f"Observers are Empty {e}")
        except Exception as e:
                logger.error(f"Error in the Observers list: {e}")
     
    def notify_Observers(self) -> None:
        self._observers[self._notificationObserverID].update(int(self._message['power']),int(self._message['status']),int(self._message['priority']))
    
    def process_Message(self,message:any)->IoTMessage:
        
        #topic = "devices/building540/NIRE_WeMo_cc_1/w3/all"
        if message['topic'].split('/')[0] == 'devices':
            self._notificationObserverID = message['topic'].split('/')[-4]+'/'+message['topic'].split('/')[-3]+'/'+message['topic'].split('/')[-2]
            self._message=message['message'][0]
            self.notify_Observers()
        elif message['topic'].split('/')[0]  =='control' :
            self._emscontroller.execute_Strategy({'controlType':message['topic'].split('/')[-1], 'cmd':message['message']})
        else:
            pass
        
    def set_EMS_Controller(self,emscontroller: EMSControl)->None:
         self._emscontroller = emscontroller

