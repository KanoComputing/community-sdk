import asyncio
import json
import uuid
from time import sleep

class RPCClient():

	def __init__(self, conn_send=None):
		self.requests = {}
		self.timeout = 500
		self.conn_send = conn_send

	def get_request_object(self, method, params=[]):
		return {
			'type': 'rpc-request',
			'id': str(uuid.uuid4()),
			'method': method,
			'params': params
		}

	def get_request_string(self, request_object):
		request_string = json.dumps(
			request_object, separators=(',', ':')
		)
		return request_string + '\r\n'

	def register_request(self, id):
		self.requests[id] = None

	def unregister_request(self, id):
		del self.requests[id]

	def set_response_data(self, id, data):
		self.requests[id] = data

	def get_response_data(self, id):
		try:
			return self.requests[id]
		except:
			return None

	def send(self, request_str):
		if self.conn_send:
			self.conn_send(request_str)

	def rpc_request(self, method, params=[]):
		request_obj = self.get_request_object(method, params)
		request_str = self.get_request_string(request_obj)
		id = request_obj['id']
		self.register_request(id)
		self.send(request_str)
		sleep(0.01)
		timeout = 0
		response = None
		while True:
			timeout += 1
			response = self.get_response_data(id)
			if response != None:
				break
			if timeout > self.timeout:
				raise TimeoutError('Request timed out')
			sleep(0.01)

		self.unregister_request(id)
		return response
