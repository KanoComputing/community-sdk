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
    battery_status = pk.get_battery_status()
    print('battery status', battery_status)
    wifi_status = pk.get_wifi_status()
    print('wifi status', wifi_status)
    available_networks = pk.scan_wifi()
    print('available networks', available_networks)
else:
    print('No Pixel Kit was found :(')
