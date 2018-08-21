const assert = require('assert');
const SerialPort = require('serialport/test');
const MockBinding = require('./util/mockbinding');
const WebSocket = require('ws');
const PixelKit = require('../src/retailpixelkit');

SerialPort.Binding = MockBinding;

const RPK_PATH = 'RPK_PATH';
const RPK_IP = '127.0.0.1';
const getMockWSServer = () => {
    const wss = new WebSocket.Server({ port: 9998 });
    return wss;
}
const getMockRPK = (path, ip) => {
    MockBinding.createPort(path, {
        vendorId: '0403',
        productId: '6015'
    });
    return new PixelKit({
        path: path,
        ip: ip
    });
};

describe('Connect to Pixel Kit', () => {
    it('Should fail if instantiating without either `path` or `ip`', (done) => {
        try {
            const rpk = new PixelKit();
            done(new Error(`Shouldn't be able to instantiate.`));
        } catch(e) {
            assert.equal(e.message, 'Path or ip address are required');
            done();
        }
    });
    it('Should resolve promise once serial connection is stablished', (done) => {
        const rpk = getMockRPK(RPK_PATH);
        rpk.connect()
            .then((device) => {
                assert.ok(device instanceof PixelKit);
                assert.ok(device.port.isOpen);
                assert.equal(device.port.path, RPK_PATH);
                MockBinding.reset();
                done();
            })
            .catch(done);
    });
    it('Should resolve promise websocket connection is stablished', (done) => {
        const rpk = getMockRPK(null, RPK_IP);
        const wss = getMockWSServer();
        rpk.connect()
            .then((device) => {
                assert.ok(device instanceof PixelKit);
                assert.equal(device.ip, RPK_IP);
                assert.equal(device.ws.readyState, WebSocket.OPEN);
                done();
                wss.close();
            })
            .catch(done);
    });
    it('Should prefer serial connection over websocket', (done) => {
        const rpk = getMockRPK(RPK_PATH, RPK_IP);
        rpk.connect()
            .then((device) => {
                assert.ok(device instanceof PixelKit);
                assert.ok(device.port.isOpen);
                assert.equal(device.port.path, RPK_PATH);
                assert.ok(!device.ip);
                assert.ok(!device.ws);
                MockBinding.reset();
                done();
            })
            .catch(done);
    });
});

describe('Send pixel kit data', () => {
    it('Should get battery status', (done) => {
        const rpk = getMockRPK(RPK_PATH);
        rpk.once('rpc-request', (data) => {
            const objRequest = JSON.parse(data);
            assert.equal(objRequest.method, 'battery-status');
            rpk.emit('rpc-response', {
                id: objRequest.id,
                err: 0,
                value: {
                    status: 'Discharging',
                    percent: '60'
                }
            });
        })
        rpk.connect()
            .then(device => device.getBatteryStatus())
            .then((data) => {
                assert.ok(!data.err);
                assert.ok(data.value.status);
                assert.ok(data.value.percent);
                MockBinding.reset();
                done();
            })
            .catch(done);
    });
    it('Should get wifi status', (done) => {
        const rpk = getMockRPK(RPK_PATH);
        rpk.once('rpc-request', (data) => {
            const objRequest = JSON.parse(data);
            assert.equal(objRequest.method, 'wifi-status');
            rpk.emit('rpc-response', {
                id: objRequest.id,
                err: 0,
                value: {
                    ssid: '',
                    mac_address: '30AEA4394048',
                    ip: '0.0.0.0',
                    port: '9998',
                    netmask: '0.0.0.0',
                    gateway: '0.0.0.0',
                    connected: false
                }
            });
        })
        rpk.connect()
        .then(device => device.getWifiStatus())
        .then((data) => {
            assert.ok(!data.err);
            assert.notEqual(data.value.ssid, undefined);
            assert.ok(data.value.mac_address);
            assert.ok(data.value.ip);
            assert.ok(data.value.port);
            assert.ok(data.value.netmask);
            assert.ok(data.value.gateway);
            assert.notEqual(data.value.connected, undefined);
            MockBinding.reset();
            done();
        })
        .catch(done);
    });
    it('Should get list of available wifi networks', (done) => {
        const rpk = getMockRPK(RPK_PATH);
        rpk.once('rpc-request', (data) => {
            const objRequest = JSON.parse(data);
            assert.equal(objRequest.method, 'wifi-scan');
            rpk.emit('rpc-response', {
                id: objRequest.id,
                err: 0,
                value: [
                    { ssid: 'NETWORK', signal: 77, security: 3 }
                ]
            });
        })
        rpk.connect()
        .then(device => device.scanWifi())
        .then((data) => {
            assert.ok(!data.err);
            assert.ok(data.value instanceof Array);
            MockBinding.reset();
            done();
        })
        .catch(done);
    });
    it('Should connect to wifi network', (done) => {
        const rpk = getMockRPK(RPK_PATH);
        rpk.once('rpc-request', (data) => {
            const objRequest = JSON.parse(data);
            assert.equal(objRequest.method, 'wifi-connect');
            rpk.emit('rpc-response', {
                id: objRequest.id,
                err: 0,
                value: {
                    ssid: 'NETWORK',
                    mac_address: '30AEA4394099',
                    ip: '192.168.0.2',
                    port: '9998',
                    netmask: '255.255.255.0',
                    gateway: '192.168.0.1',
                    connected: true,
                    signal: 70
                }
            });
        })
        rpk.connect()
        .then(device => device.connectToWifi('NETWORK', 'PASSWORD'))
        .then((data) => {
            assert.ok(!data.err);
            assert.equal(data.value.ssid, 'NETWORK');
            assert.ok(data.value.mac_address);
            assert.ok(data.value.ip);
            assert.ok(data.value.port);
            assert.ok(data.value.netmask);
            assert.ok(data.value.gateway);
            assert.ok(data.value.connected);
            MockBinding.reset();
            done();
        })
        .catch(done);
    });
    it('Should get an error when failing to connect to wifi', (done) => {
        const rpk = getMockRPK(RPK_PATH);
        rpk.once('rpc-request', (data) => {
            const objRequest = JSON.parse(data);
            assert.equal(objRequest.method, 'wifi-connect');
            rpk.emit('rpc-response', {
                id: objRequest.id,
                err: 5,
                value: null
            });
        })
        rpk.connect()
        .then(device => device.connectToWifi('NETWORK', 'BAD_PASSWORD'))
        .then((data) => {
            MockBinding.reset();
            done(new Error(`Shouldn't resolve promise.`));
        })
        .catch((err) => {
            assert.equal(err.message, 5);
            done();
        });
    });
    it('Should convert array of hexadecimal colors to rgb565/base64', () => {
        const rpk = getMockRPK(RPK_PATH);
        const expectedResult = '/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////w==';
        const hexColors = [];
        for(let i = 0; i < 128; i++) {
            hexColors.push('#FFFFFF');
        }
        const result = rpk.hexToBase64Colors(hexColors);
        assert.equal(result, expectedResult);
    });
    it('Should stream framebuffer', (done) => {
        const rpk = getMockRPK(RPK_PATH);
        const hexColors = [];
        for(let i = 0; i < 128; i++) {
            hexColors.push('#FFFFFF');
        }
        rpk.once('rpc-request', (data) => {
            const objRequest = JSON.parse(data);
            assert.equal(objRequest.method, 'lightboard:on');
            rpk.emit('rpc-response', {
                id: objRequest.id,
                err: 0
            });
        })
        rpk.connect()
            .then(device => device.streamFrame(hexColors))
            .then((data) => {
                assert.ok(!data.err);
                done();
            })
            .catch(done);
    });
});

describe('Receive pixel kit data/events', () => {
    it('Trigger correct event on button down', (done) => {
        const rpk = getMockRPK(RPK_PATH);
        const BUTTON_ID = 'js-click';
        rpk.once('button-down', (id) => {
            assert.equal(id, BUTTON_ID);
            done();
        });
        rpk.connect()
            .then((device) => {
                rpk.lineReader.emit('line', `{ "type": "event", "name": "button-down", "detail": { "button-id": "${BUTTON_ID}" } }`)
            })
            .catch(done);
    });
    it('Trigger correct event on button up', (done) => {
        const rpk = getMockRPK(RPK_PATH);
        const BUTTON_ID = 'js-click';
        rpk.once('button-up', (id) => {
            assert.equal(id, BUTTON_ID);
            done();
        });
        rpk.connect()
            .then((device) => {
                rpk.lineReader.emit('line', `{ "type": "event", "name": "button-up", "detail": { "button-id": "${BUTTON_ID}" } }`)
            })
            .catch(done);
    });
    it('Trigger correct event on mode change', (done) => {
        const rpk = getMockRPK(RPK_PATH);
        const MODE_ID = 'offline-1';
        rpk.once('dial', (id) => {
            assert.equal(id, MODE_ID);
            done();
        });
        rpk.connect()
            .then((device) => {
                rpk.lineReader.emit('line', `{ "type": "event", "name": "mode-change", "detail": { "mode-id": "${MODE_ID}" } }`)
            })
            .catch(done);
    });
    it('Trigger correct event on error message', (done) => {
        const rpk = getMockRPK(RPK_PATH);
        rpk.once('error-message', (error) => {
            assert.equal(error, 'Unexpected token b in JSON at position 0');
            done();
        });
        rpk.connect()
            .then((device) => {
                rpk.lineReader.emit('line', `bad json`)
            })
            .catch(done);
    });
});
