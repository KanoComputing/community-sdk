'''
This example will print the gesture name
'''

from communitysdk import list_connected_devices, MotionSensorKit

devices = list_connected_devices()
msk_filter = filter(lambda device: isinstance(device, MotionSensorKit), devices)
msk = next(msk_filter, None) # Get first Motion Sensor Kit

if msk == None:
	print('No Motion Sensor was found :(')
else:
	def on_gesture(gestureValue):
		print('Gesture detected:', gestureValue)
	try:
		msk.set_mode('gesture')
	except Exception as e:
		print(e)
	msk.on_gesture = on_gesture
	print('Wave your hand above the Motion Sensor:')
