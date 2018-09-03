from communitysdk import list_connected_devices
from communitysdk import RetailPixelKitSerial as PixelKit
from random import randint
from time import sleep

devices = list_connected_devices()
pk_filter = filter(lambda device: isinstance(device, PixelKit), devices)
pk = next(pk_filter, None) # Get first Pixel Kit

if pk != None:
    def print_button_down(button_id):
        print('Button {0} was pressed'.format(button_id))
    def print_button_up(button_id):
        print('Button {0} was released'.format(button_id))
    def print_dial(mode_id):
        print('Mode changed to {0}'.format(mode_id))

    pk.on_button_down = print_button_down
    pk.on_button_up = print_button_up
    pk.on_dial = print_dial

    print('Press the buttons and turn the dial mode on your Pixel Kit!')
else:
    print('No Pixel Kit was found :(')
