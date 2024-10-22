
import sys
sys.path.append("/home/sanka/NIRE_EMS/volttron/LoadPriorityControl/LPCv1/")
from Controller.ObserverSubject import ObserverSubject
from Model.Observer import Observer
from Model.IoTMessage import IoTMessage
from Model.SmartPlug import SmartPlug
from Controller.EMSControl import EMSControl
import logging

logger = logging.getLogger(__name__)

class GLEAMMMonitor(ObserverSubject):
    
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
     
    def notify_Observers(self,power,priority,status) -> None:
        self._observers[self._notificationObserverID].update(int(power),status,priority)
    
    def process_Message(self,message:any)->IoTMessage:
        
#  message= [{'C1P': 0, 'C1Q': 0, 'C1Vrms': 2840, 'C1Freq': 6000, 'PIT1': 0, 'PIT2': 0, 'PIT3': 0, 'PIT4': 0, 'PIT5': 0, 'PIT6': 0, 'PIT7': 0, 'PIT8': 0, 'PIT9': 0, 'PIT10': 0, 'AheadPIT1': 0, 'AheadPIT2': 0, 'AheadPIT3': 0, 'AheadPIT4': 0, 'AheadPIT5': 0, 'AheadPIT6': 0, 'AheadPIT7': 0, 'AheadPIT8': 0, 'AheadPIT9': 0, 'AheadPIT10': 0, 'CMDIT1': 0, 'CMDIT2': 0, 'CMDIT3': 0, 'CMDIT4': 0, 'CMDIT5': 0, 'CMDIT6': 0, 'CMDIT7': 0, 'CMDIT8': 0, 'CMDIT9': 0, 'CMDIT10': 0, 'CMDIBRK': 0, 'P-IUT': 0, 'Ahead-IUT': 0, 'Fcst-IBuilding': 0, 'CMDIT10_P': 0, 'SIT1': 1, 'SIT2': 1, 'SIT3': 1, 'SIT4': 1, 'SIT5': 1, 'SIT6': 1, 'SIT7': 1, 'SIT8': 1, 'SIT9': 1, 'SIT10': 1, 'SIBKR': 1, 'SIT10_P': 0}, {'C1P': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'C1Q': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'C1Vrms': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'C1Freq': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'PIT1': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'PIT2': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'PIT3': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'PIT4': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'PIT5': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'PIT6': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'PIT7': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'PIT8': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'PIT9': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'PIT10': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'AheadPIT1': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'AheadPIT2': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'AheadPIT3': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'AheadPIT4': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'AheadPIT5': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'AheadPIT6': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'AheadPIT7': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'AheadPIT8': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'AheadPIT9': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'AheadPIT10': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'CMDIT1': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'CMDIT2': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'CMDIT3': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'CMDIT4': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'CMDIT5': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'CMDIT6': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'CMDIT7': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'CMDIT8': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'CMDIT9': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'CMDIT10': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'CMDIBRK': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'P-IUT': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'Ahead-IUT': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'Fcst-IBuilding': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'CMDIT10_P': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'SIT1': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'SIT2': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'SIT3': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'SIT4': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'SIT5': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'SIT6': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'SIT7': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'SIT8': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'SIT9': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'SIT10': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'SIBKR': {'units': 'Kw', 'type': 'integer', 'tz': ''}, 'SIT10_P': {'units': 'Kw', 'type': 'integer', 'tz': ''}}]

        if message['topic'].split('/')[0] == 'devices':
            head=message['topic'].split('/')[-4]+'/'+message['topic'].split('/')[-3]+'/'+message['topic'].split('/')[-2]

            self._message=message['message'][0]
            for key in self._message.keys():
                self._notificationObserverID = head +'/'+key
                if self._notificationObserverID in self._observers:
                    priority=0
                    status=0
                    if 'PP' in key:
                        priority =1
                        status= self._message['SPT'+key[-2]+key[-1]] if key[-1]=='0' else  self._message['SPT'+key[-1]]
                    elif 'PC' in key:
                        priority =3
                        status= self._message['SCT'+key[-2]+key[-1]] if key[-1]=='0' else  self._message['SCT'+key[-1]]
                    elif 'PI' in key:
                        priority = 2 
                        status= self._message['SIT'+key[-2]+key[-1]] if key[-1]=='0' else  self._message['SIT'+key[-1]]

                    self.notify_Observers(self._message[key],priority,status)
        
    def set_EMS_Controller(self,emscontroller: EMSControl)->None:
         self._emscontroller = emscontroller
         
         
         
          
         

