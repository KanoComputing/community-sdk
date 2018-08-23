import serial
import asyncio
import json
from .rpcclient import RPCClient
from time import sleep

class MotionSensorKit(RPCClient):
	def __init__(self, path):
		super().__init__()
		self.path = path
		self.is_connected = False
		self.connection = serial.Serial(
			port=None,
			baudrate=115200
		)
		self.connection.dtr = True

	def connect(self):
		self.connection.port = self.path
		self.serial_connect()
		self.is_connected = True
		loop = asyncio.get_event_loop()
		loop.run_in_executor(None, self.poll_data)
		self.conn_send = self.write

	def serial_connect(self):
		if not self.connection.isOpen():
			self.connection.open()
		else:
			self.connection.close()
			self.connection.open()
		sleep(0.1)

	def close(self):
		if self.connection.isOpen():
			self.connection.close()
		self.is_connected = False

	def write(self, data):
		self.connection.write(data.encode('utf-8'))
		self.connection.flush()
		sleep(0.01)

	def poll_data(self):
		while self.is_connected:
			sleep(0.01)
			msg = self.connection.readline()
			try:
				data = json.loads(msg.decode())
				self.on_data(data)
			except Exception as e:
				pass

	def on_data(self, data):
		if data['type'] == 'rpc-response' and data['error'] == None:
			id = data['id']
			value = data['value']
			if not value:
				value = True
			self.set_response_data(id, value)
		if data['type'] == 'event':
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
