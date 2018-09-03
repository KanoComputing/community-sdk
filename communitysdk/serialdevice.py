import serial
import asyncio
import json
from .rpcclient import RPCClient
from time import sleep

class SerialDevice(RPCClient):
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
		self.loop.run_in_executor(None, self.poll_data)
		self.conn_send = self.write

	def serial_connect(self):
		if not self.connection.isOpen():
			self.connection.open()
		else:
			self.connection.close()
			self.connection.open()
		sleep(0.01)

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
			msg = self.connection.readline()
			try:
				data = json.loads(msg.decode())
				self.on_data(data)
			except Exception as e:
				pass
			sleep(0.01)

	def on_data(self, data):
		# MSK and RPK respond with different RPC formats
		err = None
		if 'error' in data.keys():
			err = data['error']
		if 'err' in data.keys():
			if data['err'] == 0:
				err = None
			else:
				err = data['err']
		if err != None:
			raise Exception('RPC response error', err)
		if data['type'] == 'rpc-response' and err == None:
			id = data['id']
			value = data['value']
			if not value:
				value = True
			self.set_response_data(id, value)
		if data['type'] == 'event':
			self.on_event(data)

	def on_event(self, data):
		pass
