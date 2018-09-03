'''
This example will scan for available networks, get battery and wifi status from
the Pixel Kit.
'''
from communitysdk import list_connected_devices
from communitysdk import RetailPixelKitSerial as PixelKit

devices = list_connected_devices()
pk_filter = filter(lambda device: isinstance(device, PixelKit), devices)
pk = next(pk_filter, None) # Get first Pixel Kit

if pk != None:
    battery_status = pk.get_battery_status()
    print('Battery status')
    print(battery_status)
    wifi_status = pk.get_wifi_status()
    print('Wifi status')
    print(wifi_status)
    available_networks = pk.scan_wifi()
    print('Available networks')
    print(available_networks)
else:
    print('No Pixel Kit was found :(')
