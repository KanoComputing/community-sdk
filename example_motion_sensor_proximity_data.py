'''
This example will print the proximity value
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
	msk.set_mode('proximity')
	msk.on_proximity = on_proximity
	print('Move your hand above the Motion Sensor:')
