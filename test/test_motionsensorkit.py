from communitysdk import MotionSensorKit, list_connected_devices
from unittest.mock import patch
import pytest

SERIAL_PATH = 'COM_TEST'
@pytest.fixture
def msk():
	with patch('communitysdk.MotionSensorKit.serial_connect'):
		m = MotionSensorKit(path=SERIAL_PATH)
		m.connect()
		yield m

def test_on_data_event(msk):
	'''
	Should fire the correct event callback when calling `on_data` with an rpc event
	'''
	proximity_event = {
		"type": "event",
		"name": "proximity-data",
		"detail": {"proximity": 127}
	}
	gesture_event = {
		"type": "event",
		"name": "gesture",
		"detail": {"type": "left"}
	}
	with patch.object(msk, 'on_proximity'),\
		patch.object(msk, 'on_gesture'):
		msk.on_data(proximity_event)
		msk.on_data(gesture_event)
		msk.on_proximity.assert_called_once_with(proximity_event['detail']['proximity'])
		msk.on_gesture.assert_called_once_with(gesture_event['detail']['type'])

def test_on_proximity_wrong(msk):
	with pytest.raises(Exception) as err:
		msk.on_proximity()
	assert "missing 1 required positional argument: 'proximity'" in str(err.value)

def test_on_gesture_wrong(msk):
	with pytest.raises(Exception) as err:
		msk.on_gesture()
	assert "missing 1 required positional argument: 'gesture'" in str(err.value)

def test_on_proximity(msk):
	msk.on_proximity('test')

def test_on_gesture(msk):
	msk.on_gesture('test')

def test_set_mode_wrong(msk):
	'''
	Should not allow unknown modes on `set_mode`
	'''
	with pytest.raises(Exception) as err:
		msk.set_mode('wrong_mode')
	assert "Invalid mode" in str(err.value)

def test_set_mode(msk):
	'''
	Should call `rpc_request` with correct data when calling `set_mode`
	'''
	with patch.object(msk, 'rpc_request'):
		msk.set_mode('proximity')
		msk.rpc_request.assert_called_once_with('set-mode', [{'mode':'proximity'}])

def test_set_interval_wrong(msk):
	'''
	Should not allow interval values that are not integers
	'''
	values = ['100', 100.1, [100]]
	for value in values:
		with pytest.raises(Exception) as err:
			msk.set_interval(value)
		assert "Interval must be an integer" in str(err.value)

def test_set_interval(msk):
	'''
	Should call `rpc_request` with correct data when calling `set_interval`
	'''
	with patch.object(msk, 'rpc_request'):
		msk.set_interval(100)
		msk.rpc_request.assert_called_once_with('set-interval', [{'interval':100}])
