from communitysdk import list_connected_devices
from communitysdk import RetailPixelKitSerial as PixelKit
from random import randint
from time import sleep

devices = list_connected_devices()
pk = None

for device in devices:
    if isinstance(device, PixelKit):
        pk = device
        break

if pk != None:
    colors = ['#ffffff', '#ff0000', '#00ff00', '#0000ff', '#ffff00', '#00ffff', '#ff00ff']
    pk.stream_frame(['#000000']*128)
    sleep(0.1)
    for color in colors:
        frame = [color]*128
        pk.stream_frame(frame)
        sleep(2)
    pk.close()
else:
    print('No Pixel Kit was found :(')
