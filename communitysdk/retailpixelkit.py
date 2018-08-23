from .serialdevice import SerialDevice
from base64 import b64encode

class RetailPixelKitSerial(SerialDevice):
	def __init__(self, path):
		super().__init__(path)

	def on_event(self, data):
		if data['name'] == 'mode-changed':
			self.on_dial(data['detail']['mode-id'])
		if data['name'] == 'button-down':
			self.on_button_down(data['detail']['button-id'])
		if data['name'] == 'button-up':
			self.on_button_up(data['detail']['button-id'])

	def on_button_up(self, buttonId):
		pass

	def on_button_down(self, buttonId):
		pass

	def on_dial(self, modeId):
		pass

	def hex_to_base64(self, hex_colors):
		int_colors = []
		for color in hex_colors:
			rgb888 = int('0x{0}'.format(color[1:]), 16)
			rgb565 = (rgb888 & 0xF8) >> 3 | (rgb888 & 0xFC00) >> 5 | (rgb888 & 0xF80000) >> 8
			int_colors.append(rgb565>>8)
			int_colors.append(rgb565&0xff)
		result = b64encode(bytes(int_colors))
		return result.decode()

	def stream_frame(self, frame):
		'''
		Just send to serial, don't wait until `rpc-response`
		'''
		if len(frame) != 128:
			raise Exception('Frame must contain 128 values')
		encodedFrame = self.hex_to_base64(frame)
		method = 'lightboard:on'
		params = [{ 'map': encodedFrame }]
		request_obj = self.get_request_object(method, params)
		request_str = self.get_request_string(request_obj)
		self.conn_send(request_str)

	def get_battery_status(self):
		return self.rpc_request('battery-status', [])

	def get_wifi_status(self):
		return self.rpc_request('wifi-status', [])

	def scan_wifi(self):
		return self.rpc_request('wifi-scan', []);

	def connect_to_wifi(self, ssid, password):
		if type(ssid) != str:
			raise Exception('`ssid` must be a string')
		if type(password) != str:
			raise Exception('`password` must be a string')
		return self.rpc_request('wifi-connect', [ssid, password])
