from communitysdk import list_connected_devices, MotionSensorKit
from communitysdk import RetailPixelKitSerial as PixelKit
from time import sleep

devices = list_connected_devices()
msk = None
rpk = None

frames = [
    ['#000000']*128, # white frame
    ['#ff0000']*128, # red frame
    ['#ffff00']*128, # yellow frame
    ['#00ff00']*128, # green frame
    ['#00ffff']*128, # cyan frame
    ['#0000ff']*128, # blue frame
    ['#ff00ff']*128 # purple frame
]

for device in devices:
    if isinstance(device, MotionSensorKit):
        msk = device
    if isinstance(device, PixelKit):
        rpk = device

if msk != None and rpk != None:
    msk.set_mode('gesture')
    print('Swipe up or down to change the color:')
    currentFrame = 0
    def on_gesture(gesture):
        global currentFrame
        print('Gesture', gesture)
        if gesture == 'up':
            currentFrame = (currentFrame+1) % len(frames)
        if gesture == 'down':
            currentFrame = (currentFrame-1) % len(frames)

    msk.on_gesture = on_gesture

    while True:
        rpk.stream_frame(frames[currentFrame])
        sleep(0.1)

else:
    print('You must have a Pixel Kit and a Motion Sensor connected for this example!')
