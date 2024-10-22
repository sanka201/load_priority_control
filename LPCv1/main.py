import sys
sys.path.append("/home/sanka/NIRE_EMS/volttron/LoadPriorityControl/LPCv1/")
from itertools import groupby
from Model.SmartPlug import SmartPlug
from Model.IoTDeviceGroup import IoTDeviceGroup
from Controller.SimpleControlStrategy import SimpleControlStrategy
from Controller.DeviceMonitor import DeviceMonitor
from Controller.DirectControl import DirectControl
from Controller.SheddingControl import SheddingControl
from Controller.IncrementalControl import IncrementalControl
from Controller.EMSControl import EMSControl
from Model.IoTDeviceGroupManager import IoTDeviceGroupManager
import sqlite3
conn = sqlite3.connect('/home/sanka/NIRE_EMS/volttron/FacadeAgent/Device_configure_database.sqlite')

def Message(topic,power,status,priority) -> dict:
    message={}
    message['topic']=topic
    message['message']=[{'power':power,'status':status,'priority':priority}]
    
    return message

def Command(topic,cmd) -> dict:
    message={}
    message['topic']=topic
    message['message']=[cmd]
    
    return message

def main():
    
        """
        This is method is called once the Agent has successfully connected to the platform.
        This is a good place to setup subscriptions if they are not dynamic or
        do any other startup activities that require a connection to the message bus.
        Called after any configurations methods that are called at startup.

        Usually not needed if using the configuration store.
        """
        # Step 2: Create a cursor object
        cursor = conn.cursor()

        # Step 3: Execute a SELECT query
        cursor.execute("SELECT * FROM devices")

        # Step 4: Fetch the results
        rows = cursor.fetchall()  # To fetch all rows
        # rows = cursor.fetchone()  # To fetch the first row
        # rows = cursor.fetchmany(10)  # To fetch the first 10 rows

        # Step 5: Work with the fetched data
        for row in rows:
            print(row[3]+'/'+row[2]+'/'+row[0])

        # Step 6: Close the cursor and connection
        cursor.close()
        conn.close()
        
        plugsid = ['w1','w2','w3', 'w4']
        command ={'building540/NIRE_WeMo_cc_1/w1':1,'building540/NIRE_WeMo_cc_1/w1':0,'building540/NIRE_WeMo_cc_1/w1':1,'building540/NIRE_WeMo_cc_1/w1':0}
        
        groupFacade = IoTDeviceGroupManager()
        group = IoTDeviceGroup() # Group Facade
        groupFacade.add_Group(group)

        
        monitor = DeviceMonitor() # Monitor for smart plug update
        controlsimple =  SimpleControlStrategy()
        controldirect = DirectControl()
        controlshed = SheddingControl()
        controlincrement = IncrementalControl()
        emscontroller = EMSControl()
        emscontroller.add_Controller(controlsimple)
        emscontroller.set_Group(group)
        emscontroller.add_Controller(controldirect)
        emscontroller.add_Controller(controlincrement)
        emscontroller.add_Controller(controlshed)
        
        
        """Assign smart Plugs to the Group Facade
        """    
        smart_plugs={}
        for row in rows:
            plug=SmartPlug(row[3]+'/'+row[2]+'/'+row[0],1)
            group.add_Device(plug)
            monitor.register_Observer(plug)
            smart_plugs[row]=plug
        print(groupFacade.group_By_Priority())
        
        
    #     """Updating Observers to update power consumption of each plug
    #     """
        
    #     monitor.set_EMS_Controller(emscontroller)
        
    #     monitor.process_Message(Message("devices/building540/NIRE_WeMo_cc_1/w1/all",200,1,2))
    #     monitor.process_Message(Message("devices/building540/NIRE_WeMo_cc_1/w2/all",20,1,2))
    #     monitor.process_Message(Message("devices/building540/NIRE_WeMo_cc_1/w3/all",500,1,1))
    #     monitor.process_Message(Message("devices/building540/NIRE_WeMo_cc_1/w4/all",400,1,5))
    #     monitor.process_Message(Command("control/building540/simple",30))
    #     monitor.process_Message(Command("control/building540/direct",command))   
    #     monitor.process_Message(Command("control/building540/shed",command)) 
    #     monitor.process_Message(Command("control/building540/increment",command))     
    
    
    #     sorted_smart_plugs_pr = sorted(
    #     smart_plugs.values(),
    #     key=lambda plug: (plug._priority),reverse=True
    #     )
        
    #     sorted_smart_plugs_p = sorted(
    #     smart_plugs.values(),
    #     key=lambda plug: (plug._power_consumptiom),reverse=True
    #     )
    # # Output the sorted list
    #     for plug in sorted_smart_plugs_pr:
    #         print(plug._priority)
        
    # # Output the sorted list
    #     for plug in sorted_smart_plugs_p:
    #         print(plug._power_consumptiom)
            
        
        #emscontroller.execute_Strategy(1)
        
        #controlsimple.execute(group,30)
        #controlsimple.execute(group,command)    
    
if __name__ == "__main__":
    
    main()
    
    
    




