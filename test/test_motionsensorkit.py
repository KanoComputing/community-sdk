from communitysdk import MotionSensorKit, list_connected_devices
from unittest.mock import patch
from time import sleep
import json
import pytest

SERIAL_PATH = 'COM_TEST'
@pytest.fixture
def msk():
    with patch('communitysdk.MotionSensorKit.serial_connect'):
        m = MotionSensorKit(path=SERIAL_PATH)
        yield m

'''
Should not instantiate without a `path`
'''
def test_require_path():
    with pytest.raises(TypeError) as err:
        msk = MotionSensorKit()
    assert "required positional argument: 'path'" in str(err.value)

'''
Should instantiate class and setup required properties
'''
def test_instance(msk):
    assert msk.path == SERIAL_PATH
    assert msk.is_connected == False
    assert msk.connection

'''
Should set `is_connected` to `True` when calling `connect`
'''
def test_connect(msk):
    msk.connect()
    assert msk.is_connected == True

'''
Should set `is_connected` to `False` when calling `close`
'''
def test_close(msk):
    msk.connect()
    assert msk.is_connected == True
    msk.close()
    assert msk.is_connected == False

'''
Should call `connection.open` when calling `connect`
'''
def test_serial_connect():
    msk = MotionSensorKit(path=SERIAL_PATH)
    with patch.object(msk.connection, 'isOpen', return_value=False),\
        patch.object(msk.connection, 'close'),\
        patch.object(msk.connection, 'open'):
        msk.connect()
        msk.connection.isOpen.assert_called()
        msk.connection.open.assert_called()
        msk.connection.close.assert_not_called()

'''
Should close connection before opening it when calling `connect` with an
open connection
'''
def test_serial_reconnect():
    msk = MotionSensorKit(path=SERIAL_PATH)
    with patch.object(msk.connection, 'isOpen', return_value=True),\
        patch.object(msk.connection, 'close'),\
        patch.object(msk.connection, 'open'):
        msk.connect()
        msk.connection.isOpen.assert_called()
        msk.connection.open.assert_called()
        msk.connection.close.assert_called()

'''
Should call `connection.write` and `connection.flush` data when calling `write`
'''
def test_write(msk):
    msk.connect()
    data = 'TEST_DATA'
    with patch.object(msk.connection, 'write'),\
        patch.object(msk.connection, 'flush'):
        msk.write(data)
        msk.connection.write.assert_called_once_with(data.encode('utf-8'))
        msk.connection.flush.assert_called_once()

'''
Should replace `conn_send` with `write` when calling `connect`
'''
def test_conn_send(msk):
    msk.connect()
    assert msk.conn_send == msk.write

'''
Should start polling data after connect
'''
def test_conn_send(msk):
    with patch.object(msk, 'poll_data'):
        msk.connect()
        sleep(0.02) # Polls data every 0.01 seconds after connecting
        msk.poll_data.assert_called()

'''
Should read line, parse data into a json object and call `on_data` when
polling data
'''
def test_poll_data(msk):
    line = b'{"success":"true"}\r\n'
    msg = json.loads(line.decode())
    with patch.object(msk.connection, 'readline', return_value=line),\
        patch.object(msk, 'on_data'):
        msk.connect()
        sleep(0.02) # Polls data every 0.01 seconds after connecting
        msk.connection.readline.assert_called()
        msk.on_data.assert_called_with(msg)

'''
Should set response data when calling `on_data` with an rpc response
'''
def test_on_data_response(msk):
    rpc_response = {
        "id": "fake-id",
        "type": "rpc-response",
        "error": None,
        "value": ["result"]
    }
    msk.on_data(rpc_response)
    data = msk.get_response_data(rpc_response['id'])
    assert data == rpc_response['value']

'''
Should fire the correct event callback when calling `on_data` with an rpc event
'''
def test_on_data_event(msk):
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

'''
Should not allow unknown modes on `set_mode`
'''
def test_set_mode_wrong(msk):
    with pytest.raises(Exception) as err:
        msk.set_mode('wrong_mode')
    assert "Invalid mode" in str(err.value)

'''
Should call `rpc_request` with correct data when calling `set_mode`
'''
def test_set_mode(msk):
    with patch.object(msk, 'rpc_request'):
        msk.set_mode('proximity')
        msk.rpc_request.assert_called_once_with('set-mode', [{'mode':'proximity'}])

'''
Should not allow interval values that are not integers
'''
def test_set_interval_wrong(msk):
    values = ['100', 100.1, [100]]
    for value in values:
        with pytest.raises(Exception) as err:
            msk.set_interval(value)
        assert "Interval must be an integer" in str(err.value)

'''
Should call `rpc_request` with correct data when calling `set_interval`
'''
def test_set_interval(msk):
    with patch.object(msk, 'rpc_request'):
        msk.set_interval(100)
        msk.rpc_request.assert_called_once_with('set-interval', [{'interval':100}])
