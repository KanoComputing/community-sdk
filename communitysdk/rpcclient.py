import asyncio
import json
import uuid
from time import sleep

class RPCClient():

	def __init__(self, conn_send=None):
		self.requests = {}
		self.timeout = 500
		self.conn_send = conn_send
		self.loop = asyncio.get_event_loop()

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

	@asyncio.coroutine
	def wait_for_response(self, id):
		'''
		Wait until there is data in the `requests` dictionary for a given id/key
		and set it as the result of the given `Future`.
		'''
		t = 0
		while True:
			t += 1
			if t > self.timeout:
				raise TimeoutError('Request timed out')
			if self.get_response_data(id) != None:
				# Return the value
				return self.get_response_data(id)
			yield from asyncio.sleep(0.01)

	@asyncio.coroutine
	def send(self, request_str):
		if self.conn_send:
			self.conn_send(request_str)

	def rpc_request(self, method, params=[]):
		request_obj = self.get_request_object(method, params)
		request_str = self.get_request_string(request_obj)
		id = request_obj['id']
		self.register_request(id)

		asyncio.set_event_loop(self.loop)

		tasks = asyncio.gather(
			self.send(request_str),
			self.wait_for_response(id)
		)
		self.loop.run_until_complete(tasks)

		result = self.get_response_data(id)
		self.unregister_request(id)
		return result
