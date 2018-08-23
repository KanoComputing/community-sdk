import asyncio
import json
import uuid

class RPCClient():

	def __init__(self, conn_send=None):
		self.requests = {}
		self.timeout = 1000 * 5 # ~5 seconds timeout
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

	async def wait_for_response(self, future, id):
		'''
		Wait until there is data in the `requests` dictionary for a given id/key
		and set it as the result of the given `Future`.
		'''
		t = 0
		while True:
			t += 1
			if t > self.timeout:
				future.cancel()
				break
			if self.get_response_data(id) != None:
				# Set the future result
				future.set_result(self.requests[id])
				break
			await asyncio.sleep(0.001)

	async def send(self, request_str):
		if self.conn_send:
			self.conn_send(request_str)

	def rpc_request(self, method, params=[]):
		request_obj = self.get_request_object(method, params)
		request_str = self.get_request_string(request_obj)
		id = request_obj['id']
		self.register_request(id)
		future = asyncio.Future()
		loop = asyncio.get_event_loop()
		todo = asyncio.gather(
			self.send(request_str),
			asyncio.ensure_future( self.wait_for_response(future, id) )
		)
		loop.run_until_complete(todo)
		self.unregister_request(id)
		return future.result()
