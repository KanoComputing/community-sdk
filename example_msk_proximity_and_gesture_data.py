'''
This example will switch to `gesture` mode when you move your hand close to the
Motion Sensor Kit and will switch back to `proximity` mode when it recognizes
the gesture "up".
'''

from communitysdk import list_connected_devices, MotionSensorKit

devices = list_connected_devices()
msk_filter = filter(lambda device: isinstance(device, MotionSensorKit), devices)
msk = next(msk_filter, None) # Get first Motion Sensor Kit

if msk == None:
    print('No Motion Sensor was found :(')
else:
    def on_proximity(proximityValue):
        # Avoid printing `0` all the time
        if proximityValue > 0:
            print('Proximity value:', proximityValue)
        if proximityValue > 250:
            print('Changing now to gesture mode.')
            try:
                msk.set_mode('gesture')
            except Exception as e:
                print(e)
            print('Swipe your hand above the sensor. Swipe "up" to change to proximity mode.')

    def on_gesture(gestureValue):
        print('Gesture detected:', gesture)
        if gestureValue == 'up':
            print('Changing now to proximity mode.')
            msk.set_mode('proximity')
            print('Move your hand close to the sensor to change to gesture mode.')

    msk.set_mode('proximity')
    msk.on_proximity = on_proximity
    msk.on_gesture = on_gesture
    print('Move your hand above the Motion Sensor:')
