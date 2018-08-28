from communitysdk import RPCClient
from time import sleep
import asyncio
import json
import pytest
from unittest.mock import patch

@pytest.fixture()
def client():
	client = RPCClient()
	yield client

def test_request_object(client):
	'''
	Should get valid request object
	'''
	method = 'method'
	params = ['param']
	request_obj = client.get_request_object(method, params)
	assert request_obj['id']
	assert request_obj['type'] == 'rpc-request'
	assert request_obj['method'] == method
	assert request_obj['params'] == params

def test_request_string(client):
	'''
	Should get valid request string
	'''
	request_obj = {
		"id": "test-id",
		"type": "rpc-request",
		"method": "test-method",
		"params": ["param"]
	}
	request_str = client.get_request_string(request_obj)
	assert request_str == json.dumps(request_obj, separators=(',', ':'))+'\r\n'

def test_register_request(client):
	'''
	Should register request
	'''
	id = 'test-id'
	client.register_request(id)
	assert id in client.requests.keys()
	assert client.requests[id] == None

def test_unregister_request(client):
	'''
	Should unregister request
	'''
	id = 'test-id'
	client.register_request(id)
	assert id in client.requests.keys()
	assert client.requests[id] == None
	client.unregister_request(id)
	assert not (id in client.requests.keys())

def test_set_response_data(client):
	'''
	Should set response data
	'''
	id = "test-id"
	data = {"success": True}
	client.set_response_data(id, data)
	assert client.requests[id] == data

def test_get_response_data(client):
	'''
	Should get response data
	'''
	id = "test-id"
	data = {"success": True}
	# Should be `None` if response is not set
	emptyData = client.get_response_data(id)
	assert emptyData == None
	client.set_response_data(id, data)
	response_data = client.get_response_data(id)
	assert data == response_data

def test_wait_for_response(client):
	'''
	Should wait until the value of a given key (`id`) on the `requests` dictionary
	is set to something different than `None` then set this value as the result
	of the `Future`.
	'''
	id = 'test-id'
	data = {"success": True}
	client.register_request(id)
	# Schedule to set the response data after 0.1 seconds
	def set_value():
		sleep(0.1)
		client.set_response_data(id, data)
	loop = asyncio.get_event_loop()
	pollingFuture = loop.run_in_executor(None, set_value)
	# Wait for the response data to be filled
	future = asyncio.Future()
	loop.run_until_complete(
		asyncio.ensure_future( client.wait_for_response(future, id) )
	)
	assert future.result() == data

def test_wait_for_response_timeout(client):
	'''
	Timeout when response takes more than the threshold
	'''
	id = 'test-id'
	data = {"success": True}
	client.timeout = 100
	client.register_request(id)
	loop = asyncio.get_event_loop()
	future = asyncio.Future()
	loop.run_until_complete(
		asyncio.ensure_future( client.wait_for_response(future, id) )
	)
	assert future.cancelled() == True

def test_rpc_request(client):
	'''
	Should return `rpc_request` call with the result once data is set on
	`requests` object and unregister the request
	'''
	response_data = {"success": True}
	def conn_send(msg):
		data = json.loads(msg)
		client.set_response_data(data['id'], response_data)
	with patch.object(client, 'conn_send', side_effect=conn_send):
		result = client.rpc_request('method', ['param'])
		assert result == response_data
		assert client.requests == {}

def test_conn_send(client):
	'''
	Should call `conn_send` when making a `rpc_request`
	'''
	def conn_send(msg):
		data = json.loads(msg)
		client.set_response_data(data['id'], True)
	with patch.object(client, 'conn_send', side_effect=conn_send):
		result = client.rpc_request('method', ['params'])
		client.conn_send.assert_called()
