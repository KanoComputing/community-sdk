'''
This example will print the proximity value and the rate of change on proximity
value in a format that can be used to plot graphs on Mu Editor.
'''

from communitysdk import list_connected_devices, MotionSensorKit

devices = list_connected_devices()
msk = None

for device in devices:
    if isinstance(device, MotionSensorKit):
        msk = device
        break

if msk != None:
    previous_value = 0
    def on_proximity(proximity):
        global previous_value
        delta = proximity - previous_value
        print((proximity, delta))
        previous_value = proximity
    print('Move your hand above the Motion Sensor:')
    msk.set_mode('proximity')
    msk.on_proximity = on_proximity
else:
    print('No Motion Sensor was found :(')
