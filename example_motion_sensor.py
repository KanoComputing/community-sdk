from communitysdk import list_connected_devices, MotionSensorKit

devices = list_connected_devices()
msk = None

for device in devices:
    if isinstance(device, MotionSensorKit):
        msk = device
        break

if msk == None:
    print('No Motion Sensor was found :(')
else:

    def on_proximity(proximity):
        print('proximity', proximity)
        if proximity > 250:
            print('Changing now to gesture mode')
            try:
                msk.set_mode('gesture')
            except Exception as e:
                print(e)
            print('Swipe your hand above the sensor. Swipe "up" to change to proximity mode.')

    def on_gesture(gesture):
        print('gesture', gesture)
        if gesture == 'up':
            print('Changing now to proximity mode')
            msk.set_mode('proximity')
            print('Move your hand close to the sensor to change to gesture mode.')

    msk.set_mode('proximity')
    msk.on_proximity = on_proximity
    msk.on_gesture = on_gesture
    print('Move your hand above the Motion Sensor:')
