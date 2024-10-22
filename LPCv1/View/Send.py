
import sys
import time
sys.path.append("/home/sanka/NIRE_EMS/volttron/LoadPriorityControl/LPCv1/")
from View.Publish import Publish
from Model.IoTMessage import IoTMessage
class Send(Publish):
    def __init__(self,vip) -> None:
        super().__init__()
        self._vip=vip
        
    def publish(self, message: IoTMessage, deviceType:str) -> bool:
        print("Sending",message)
        if deviceType=='plug':
           result=self._vip.rpc.call('platform.driver','set_point',message.device_id,'status',message.payload['cmd'],external_platform=message.device_id.split('/')[-2])
        elif deviceType == 'EV':
           result=self._vip.rpc.call('platform.driver','set_point',message.device_id,'cmd1',message.payload['cmd'])
        elif deviceType == 'gleammrload':
            temp=message.device_id.split('/')
            if 'PPT' in message.device_id:
                topic= 'Microgrid/GLEAMM/BuildingP'
                control= 'CMDPT'+temp[-1][-2]+temp[-1][-1]if temp[-1][-1]=='0' else 'CMDPT'+temp[-1][-1]
                breaker = 'CMDPBRK'
                
            elif  'PCT' in message.device_id:
                topic= 'Microgrid/GLEAMM/BuildingC'
                control= 'CMDCT'+temp[-1][-2]+temp[-1][-1]if temp[-1][-1]=='0' else 'CMDCT'+temp[-1][-1]
                breaker = 'CMDCBRK'
            elif 'PIT' in message.device_id:
                topic= 'Microgrid/GLEAMM/BuildingI'
                control= 'CMDIT'+temp[-1][-2]+temp[-1][-1]if temp[-1][-1]=='0' else 'CMDIT'+temp[-1][-1]  
                breaker = 'CMDIBRK'     
            print("_________________^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^",topic,control)         
            result=self._vip.rpc.call('platform.driver','set_point',topic,control,message.payload['cmd'])
            time.sleep(.5)
            result=self._vip.rpc.call('platform.driver','set_point',topic,breaker,1)