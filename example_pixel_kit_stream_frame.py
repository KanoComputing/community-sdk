'''
This example will stream a series of single color "frames" to Pixel Kit.
'''
from communitysdk import list_connected_devices
from communitysdk import RetailPixelKitSerial as PixelKit
from time import sleep

devices = list_connected_devices()
pk_filter = filter(lambda device: isinstance(device, PixelKit), devices)
pk = next(pk_filter, None) # Get first Pixel Kit

if pk != None:
	'''
	A frame is an array of 128 hexadecimal colors prefixed with `#`.
	We'll create a single color frame (all the pixels with the same
	color) to stream to Pixel Kit.
	'''
	# `[value] * number` is a shortcut to create and array with `number` times the `value` element
	frame = ['#ffff00']*128 # Yellow frame
	'''
	We will send a frame every 0.1 seconds to Pixel Kit (10 frames
    per second). It's important to keep sending frames to the Pixel Kit,
    otherwise it will go back to the mode it was before.
	'''
	while True:
		pk.stream_frame(frame)
		sleep(0.1)
else:
	print('No Pixel Kit was found :(')
