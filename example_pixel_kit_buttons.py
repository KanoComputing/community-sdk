from communitysdk import list_connected_devices
from communitysdk import RetailPixelKitSerial as PixelKit
from random import randint
from time import sleep

devices = list_connected_devices()
pk = None

colors = ['#ffffff', '#ff0000', '#00ff00', '#0000ff', '#ffff00', '#00ffff', '#ff00ff']
frames = []
for color in colors:
    frames.append([color]*128)
currentFrame = 0

for device in devices:
    if isinstance(device, PixelKit):
        pk = device
        break

if pk != None:
    def print_button(button_id):
        global currentFrame
        print('Button', button_id, 'was pressed down')
        currentFrame = (currentFrame + 1) % len(frames)

    pk.on_button_down = print_button

    pk.stream_frame(['#000000']*128)
    sleep(0.1)
    while True:
        pk.stream_frame(frames[currentFrame])
        sleep(0.1)
else:
    print('No Pixel Kit was found :(')
