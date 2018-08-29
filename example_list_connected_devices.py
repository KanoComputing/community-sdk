'''
This example will list all the available/connected Kano devices and filter it
by its classes.
'''

from communitysdk import list_connected_devices, MotionSensorKit,\
    RetailPixelKitSerial as PixelKit

devices = list_connected_devices()

msk_filter = filter(lambda device: isinstance(device, MotionSensorKit), devices)
rpk_filter = filter(lambda device: isinstance(device, PixelKit), devices)

available_msk = list(msk_filter)
available_rpk = list(rpk_filter)

print('Found {0} devices'.format(len(devices)))
print('Found {0} Motion Sensor Kits'.format(len(available_msk)))
print('Found {0} Pixel Kits'.format(len(available_rpk)))
