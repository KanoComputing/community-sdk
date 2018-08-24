from communitysdk import list_connected_devices, MotionSensorKit

devices = list_connected_devices()
msk = None

for device in devices:
    if isinstance(device, MotionSensorKit):
        msk = device
        break

if msk != None:
    print('Move your hand above the Motion Sensor:')
    msk.set_mode('proximity')
    # print('Swipe your hand above the Motion Sensor:')
    # msk.set_mode('gesture')

    def on_proximity(proximity):
        print('proximity', proximity)
    def on_gesture(gesture):
        print('gesture', gesture)
    msk.on_proximity = on_proximity
    msk.on_gesture = on_gesture
else:
    print('No Motion Sensor was found :(')
