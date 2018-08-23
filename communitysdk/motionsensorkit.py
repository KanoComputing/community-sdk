import serial
import asyncio
import json
from .serialdevice import SerialDevice
from time import sleep

class MotionSensorKit(SerialDevice):
	def __init__(self, path):
		super().__init__(path)

	def on_event(self, data):
		if data['name'] == 'proximity-data':
			self.on_proximity(data['detail']['proximity'])
		elif data['name'] == 'gesture':
			self.on_gesture(data['detail']['type'])

	def on_proximity(self, proximity):
		pass

	def on_gesture(self, gesture):
		pass

	def set_mode(self, mode):
		if mode != 'proximity' and mode != 'gesture':
			raise Exception('Invalid mode')
		return self.rpc_request('set-mode', [{'mode': mode}])

	def set_interval(self, interval):
		if type(interval) != int:
			raise Exception('Interval must be an integer')
		return self.rpc_request('set-interval', [{'interval': interval}])
