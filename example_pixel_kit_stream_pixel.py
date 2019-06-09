"""
This example will stream a single color pixel to Pixel Kit.
"""
from communitysdk import list_connected_devices
from communitysdk import RetailPixelKitSerial as PixelKit
from communitysdk.retailpixelkit import COLUMNS, ROWS
from random import randint
from time import sleep

devices = list_connected_devices()
pk_filter = filter(lambda device: isinstance(device, PixelKit), devices)
pk = next(pk_filter, None)  # Get first Pixel Kit


def get_random_hex() -> str:
    random_number = randint(0, 16777215)  # number of possible colors
    hex_number = str(hex(random_number))
    hex_number = '#{}'.format(hex_number[2:])
    return hex_number


def get_random_pixel() -> tuple:
    x = randint(1, COLUMNS)
    y = randint(1, ROWS)
    color = get_random_hex()
    return x, y, color


if pk is not None:
    """
    A pixel is a tuple with an x and y coordinate and a hexadecimal color
    prefixed with `#`. 
    We'll create a random color and coordinate to stream to the Pixel Kit.
    """
    while True:
        pixels = [get_random_pixel()]
        pk.stream_pixels(pixels)
        sleep(0.1)
else:
    print('No Pixel Kit was found :(')
