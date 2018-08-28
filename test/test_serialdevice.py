from communitysdk.serialdevice import SerialDevice
from unittest.mock import patch
from time import sleep
import json
import pytest
import asyncio

SERIAL_PATH = 'COM_TEST'
@pytest.fixture
def device():
	with patch('communitysdk.SerialDevice.serial_connect'):
		d = SerialDevice(path=SERIAL_PATH)
		yield d

def test_require_path():
	'''
	Should not instantiate without a `path`
	'''
	with pytest.raises(TypeError) as err:
		device = SerialDevice()
	assert "required positional argument: 'path'" in str(err.value)

def test_instance(device):
	'''
	Should instantiate class and setup required properties
	'''
	assert device.path == SERIAL_PATH
	assert device.is_connected == False
	assert device.connection

def test_is_connected_connect(device):
	'''
	Should set `is_connected` to `True` when calling `connect`
	'''
	device.connect()
	assert device.is_connected == True

def test_is_connected_close(device):
	'''
	Should set `is_connected` to `False` when calling `close`
	'''
	device.is_connected = True
	device.close()
	assert device.is_connected == False

def test_serial_connect():
	'''
	Should call `connection.open` when calling `connect`
	'''
	device = SerialDevice(path=SERIAL_PATH)
	with patch.object(device.connection, 'isOpen', return_value=False),\
		patch.object(device.connection, 'close'),\
		patch.object(device.connection, 'open'):
		device.connect()
		device.connection.isOpen.assert_called()
		device.connection.open.assert_called()
		device.connection.close.assert_not_called()

def test_serial_reconnect():
	'''
	Should close connection before opening it when calling `connect` with an
	open connection
	'''
	device = SerialDevice(path=SERIAL_PATH)
	with patch.object(device.connection, 'isOpen', return_value=True),\
		patch.object(device.connection, 'close'),\
		patch.object(device.connection, 'open'):
		device.connect()
		device.connection.isOpen.assert_called()
		device.connection.open.assert_called()
		device.connection.close.assert_called()

def test_close(device):
	'''
	Should call `connection.close` when calling `close`
	'''
	with patch.object(device.connection, 'isOpen', return_value=True),\
		patch.object(device.connection, 'close'):
		device.close()
		device.connection.close.assert_called()

def test_write(device):
	'''
	Should call `connection.write` and `connection.flush` data when calling `write`
	'''
	device.connect()
	data = 'TEST_DATA'
	with patch.object(device.connection, 'write'),\
		patch.object(device.connection, 'flush'):
		device.write(data)
		device.connection.write.assert_called_once_with(data.encode('utf-8'))
		device.connection.flush.assert_called_once()

def test_conn_send(device):
	'''
	Should replace `conn_send` with `write` when calling `connect`
	'''
	device.connect()
	assert device.conn_send == device.write

def test_conn_send(device):
	'''
	Should start polling data after connect
	'''
	with patch.object(device, 'poll_data'):
		device.connect()
		sleep(0.02) # Polls data every 0.01 seconds after connecting
		device.poll_data.assert_called()

def test_poll_data(device):
	'''
	Should read line, parse data into a json object and call `on_data` when
	polling data
	'''
	line = b'{"success":"true"}\r\n'
	msg = json.loads(line.decode())
	with patch.object(device.connection, 'readline', return_value=line),\
		patch.object(device, 'on_data'):
		device.connect()
		sleep(0.02) # Polls data every 0.01 seconds after connecting
		device.connection.readline.assert_called()
		device.on_data.assert_called_with(msg)

def test_poll_data_bad_json(device):
	'''
	Should ignore bad json data coming from serial and not call `on_data`
	'''
	line = b'BAD JSON'
	with patch.object(device.connection, 'readline', return_value=line),\
		patch.object(device, 'on_data'):
		device.connect()
		sleep(0.02) # Polls data every 0.01 seconds after connecting
		device.on_data.assert_not_called()

def test_on_data_response_msk(device):
	'''
	Should set response data when calling `on_data` with an rpc response
	'''
	rpc_response = {
		"id": "fake-id",
		"type": "rpc-response",
		"error": None,
		"value": ["result"]
	}
	device.on_data(rpc_response)
	data = device.get_response_data(rpc_response['id'])
	assert data == rpc_response['value']

def test_on_data_response_error_msk(device):
	'''
	Should raise exception when calling `on_data` with an rpc response with error
	'''
	rpc_response = {
		"id": "fake-id",
		"type": "rpc-response",
		"error": "Error message",
		"value": ["result"]
	}
	with pytest.raises(Exception) as err:
		device.on_data(rpc_response)
	assert "RPC response error" in str(err.value)

def test_on_data_response_rpk(device):
	'''
	Should set response data when calling `on_data` with an rpc response
	'''
	rpc_response = {
		"id": "fake-id",
		"type": "rpc-response",
		"err": 0,
		"value": ["result"]
	}
	device.on_data(rpc_response)
	data = device.get_response_data(rpc_response['id'])
	assert data == rpc_response['value']

def test_on_data_response_error_rpk(device):
	'''
	Should set response data when calling `on_data` with an rpc response
	'''
	rpc_response = {
		"id": "fake-id",
		"type": "rpc-response",
		"err": 1,
		"value": ["result"]
	}
	with pytest.raises(Exception) as err:
		device.on_data(rpc_response)
	assert "RPC response error" in str(err.value)

def test_on_data_event(device):
	'''
	Should call `on_event` when calling `on_data` with an rpc event
	'''
	event = {
		"type": "event",
		"name": "eventname",
		"detail": {"number": 127}
	}
	with patch.object(device, 'on_event'):
		device.on_data(event)
		device.on_event.assert_called_once_with(event)

def test_on_data_without_value(device):
	'''
	Should set response `True` when calling `on_data` with an rpc response
	without value
	'''
	rpc_response = {
		"id": "fake-id",
		"type": "rpc-response",
		"err": 0,
		"value": None
	}
	device.on_data(rpc_response)
	data = device.get_response_data(rpc_response['id'])
	assert data == True

def test_on_event_wrong(device):
	with pytest.raises(TypeError) as err:
		device.on_event()
	assert "missing 1 required positional argument: 'data'" in str(err.value)

def test_on_event(device):
	data = {
		"type": "event",
		"name": "test",
		"value": None
	}
	device.on_event(data)

def test_on_data_make_new_request(device):
	'''
	Should be able to make a new rpc request inside the `on_data` callback
	'''
	line = [b'{"type": "event","name": "eventname","detail": {"number": 127}}\r\n']
	def conn_send(msg):
		data = json.loads(msg)
		device.set_response_data(data['id'], True)
	with patch.object(device, 'serial_connect'),\
		patch.object(device.connection, 'readline', side_effect=line),\
		patch.object(device, 'write', side_effect=conn_send):
		loop = asyncio.get_event_loop()
		future = asyncio.Future()
		def on_event(data):
			response = device.rpc_request('method', ['param'])
			future.set_result(response)
		device.on_event = on_event
		device.connect()
		sleep(0.02) # Needs to wait > then 0.01 seconds to connect and start polling data
		assert future.result()
