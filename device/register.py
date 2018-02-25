'''
Created on 25-Feb-2018

@author: Arvind
'''

import sys
import iothub_service_client
from iothub_service_client import IoTHubRegistryManager, IoTHubRegistryManagerAuthMethod
from iothub_service_client import IoTHubDeviceStatus, IoTHubError


DeviceID = "abcd"


CONNECTION_STRING = "HostName=psg.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=xadV+l5hi1IwxmO5fxHFWThAHTrpaBGe0fI5UnTvz9c="

def print_device_info(title, iothub_device):
    print ( title + ":" )
    print ( "iothubDevice.deviceId                    = {0}".format(iothub_device.deviceId) )
    print ( "iothubDevice.primaryKey                  = {0}".format(iothub_device.primaryKey) )
    print ( "" )
    
iothub_registry_manager = IoTHubRegistryManager(CONNECTION_STRING)

device_info = (iothub_registry_manager.get_device(DeviceID))

print_device_info("DEVICE:"+DeviceID, device_info)
