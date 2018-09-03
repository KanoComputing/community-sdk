from communitysdk import RetailPixelKitSerial as PixelKit
from communitysdk import list_connected_devices
from unittest.mock import patch
import pytest

SERIAL_PATH = 'COM_TEST'
@pytest.fixture
def rpk():
	with patch('communitysdk.RetailPixelKitSerial.serial_connect'):
		pk = PixelKit(path=SERIAL_PATH)
		pk.connect()
		yield pk

def test_on_data_event(rpk):
	'''
	Should fire the correct event callback when calling `on_data` with an rpc event
	'''
	button_up = {
		"type": "event",
		"name": "button-up",
		"detail": {"button-id": "js-click"}
	}
	button_down = {
		"type": "event",
		"name": "button-down",
		"detail": {"button-id": "js-click"}
	}
	mode_changed = {
		"type": "event",
		"name": "mode-change",
		"detail": {"mode-id": "offline-1"}
	}
	with patch.object(rpk, 'on_button_down'),\
		patch.object(rpk, 'on_button_up'),\
		patch.object(rpk, 'on_dial'):
		rpk.on_data(button_down)
		rpk.on_data(button_up)
		rpk.on_data(mode_changed)
		rpk.on_button_down.assert_called_once_with(button_down['detail']['button-id'])
		rpk.on_button_up.assert_called_once_with(button_up['detail']['button-id'])
		rpk.on_dial.assert_called_once_with(mode_changed['detail']['mode-id'])

def test_on_button_up_wrong(rpk):
	'''
	Should raise exception when calling `on_button_up` without argument
	'''
	with pytest.raises(Exception) as err:
		rpk.on_button_up()
	assert "missing 1 required positional argument: 'buttonId'" in str(err.value)

def test_on_button_down_wrong(rpk):
	'''
	Should raise exception when calling `on_button_down` without argument
	'''
	with pytest.raises(Exception) as err:
		rpk.on_button_down()
	assert "missing 1 required positional argument: 'buttonId'" in str(err.value)

def test_on_dial_wrong(rpk):
	'''
	Should raise exception when calling `on_dial` without argument
	'''
	with pytest.raises(Exception) as err:
		rpk.on_dial()
	assert "missing 1 required positional argument: 'modeId'" in str(err.value)

def test_on_button_up(rpk):
	'''
	Should not raise exception when calling `on_button_up` with argument
	'''
	rpk.on_button_up('test')

def test_on_button_down(rpk):
	'''
	Should not raise exception when calling `on_button_down` with argument
	'''
	rpk.on_button_down('test')

def test_on_dial(rpk):
	'''
	Should not raise exception when calling `on_dial` with argument
	'''
	rpk.on_dial('test')

def test_hex_to_base64(rpk):
	'''
	Should convert array of hexadecimal colors to base64 string
	'''
	expected =  '/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////w==';
	frame = ['#ffffff'] * 128
	encodedFrame = rpk.hex_to_base64(frame)
	assert encodedFrame == expected

def test_stream_frame_wrong(rpk):
	'''
	Should not raise exception when calling `stream_frame` with array with less
	then 128 items
	'''
	with pytest.raises(Exception) as err,\
		patch.object(rpk, 'conn_send'):
		frame = ['#ffffff'] * 127
		rpk.stream_frame(frame)
	assert "Frame must contain 128 values" in str(err.value)

def test_stream_frame(rpk):
	'''
	Should call `conn_send` instead of `rpc_response` when streaming frame to
	avoid blocking execution and getting more frames per second
	'''
	with patch.object(rpk, 'conn_send'),\
		patch.object(rpk, 'rpc_request'):
		frame = ['#ffffff'] * 128
		rpk.stream_frame(frame)
		rpk.conn_send.assert_called_once()
		rpk.rpc_request.assert_not_called()

def test_get_battery_status(rpk):
	'''
	Should call `rpc_request` with correct arguments
	'''
	with patch.object(rpk, 'rpc_request'):
		rpk.get_battery_status()
		rpk.rpc_request.assert_called_once_with('battery-status', [])

def test_get_wifi_status(rpk):
	'''
	Should call `rpc_request` with correct arguments
	'''
	with patch.object(rpk, 'rpc_request'):
		rpk.get_wifi_status()
		rpk.rpc_request.assert_called_once_with('wifi-status', [])

def test_scan_wifi(rpk):
	'''
	Should call `rpc_request` with correct arguments
	'''
	with patch.object(rpk, 'rpc_request'):
		rpk.scan_wifi()
		rpk.rpc_request.assert_called_once_with('wifi-scan', [])

def test_connect_to_wifi(rpk):
	'''
	Should call `rpc_request` with correct arguments
	'''
	with patch.object(rpk, 'rpc_request'):
		ssid = 'NETWORK'
		password = 'PASSWORD'
		rpk.connect_to_wifi(ssid, password)
		rpk.rpc_request.assert_called_once_with('wifi-connect', [ssid, password])

def test_connect_to_wifi_wrong(rpk):
	'''
	Should raise exceptions when missing arguments or using arguments with wrong
	type to connect to wifi
	'''
	ssid = 'NETWORK'
	password = 'PASSWORD'
	wrong_values = [123, [123], True, ['123'], {"value": 1}]
	with pytest.raises(Exception) as err,\
		patch.object(rpk, 'rpc_request'):
		rpk.connect_to_wifi()
	assert "missing 2 required positional arguments: 'ssid' and 'password'" in str(err.value)
	with pytest.raises(Exception) as err,\
		patch.object(rpk, 'rpc_request'):
		rpk.connect_to_wifi(ssid)
	assert "missing 1 required positional argument: 'password'" in str(err.value)
	for value in wrong_values:
		with pytest.raises(Exception) as err,\
			patch.object(rpk, 'rpc_request'):
			rpk.connect_to_wifi(value, password)
		assert "`ssid` must be a string" in str(err.value)
	for value in wrong_values:
		with pytest.raises(Exception) as err,\
			patch.object(rpk, 'rpc_request'):
			rpk.connect_to_wifi(ssid, value)
		assert "`password` must be a string" in str(err.value)
