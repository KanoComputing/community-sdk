const assert = require('assert');
const SerialPort = require('serialport/test');
const MockBinding = require('./util/mockbinding');
const MotionSensor = require('../src/motionsensorkit');

SerialPort.Binding = MockBinding;

const MSK_PATH = 'MSK_PATH';
const getMockMSK = () => {
    MockBinding.createPort(MSK_PATH, {
        vendorId: '2341',
        productId: '814e'
    });
    return new MotionSensor({
        path: MSK_PATH,
        SerialChannel: SerialPort
    });
}

describe('Send and receive motion sensor data', () => {
    it('Resolve promise once serial connection is stablished', (done) => {
        const msk = getMockMSK();
        msk.connect()
            .then((device) => {
                assert.ok(device);
                assert.ok(device instanceof MotionSensor);
                assert.equal(device.port.path, MSK_PATH);
                MockBinding.reset();
                done();
            })
            .catch(done);
    });
    it('Set mode to proximity', (done) => {
        const msk = getMockMSK();
        msk.once('rpc-request', (data) => {
            const objRequest = JSON.parse(data);
            assert.equal(objRequest.method, 'set-mode');
            assert.equal(objRequest.params[0].mode, 'proximity');
            msk.emit('rpc-response', {
                id: objRequest.id,
                err: null,
                value: null
            });
        });
        msk.connect()
            .then(device => device.setMode('proximity'))
            .then((result) => {
                MockBinding.reset();
                if(result.err != null) {
                    done(new Error(result.err));
                } else {
                    MockBinding.reset();
                    done()
                }
            })
            .catch(done);
    });
    it('Set mode to gesture', (done) => {
        const msk = getMockMSK();
        msk.once('rpc-request', (data) => {
            const objRequest = JSON.parse(data);
            assert.equal(objRequest.method, 'set-mode');
            assert.equal(objRequest.params[0].mode, 'gesture');
            msk.emit('rpc-response', {
                id: objRequest.id,
                err: null,
                value: null
            });
        });
        msk.connect()
            .then(device => device.setMode('gesture'))
            .then((result) => {
                if(result.err != null) {
                    done(new Error(result.err));
                } else {
                    MockBinding.reset();
                    done();
                }
            })
            .catch(done);
    });
    it('Fail setting wrong mode', (done) => {
        const msk = getMockMSK();
        msk.connect()
            .then(device => device.setMode('telekinesis'))
            .then((result) => {
                done(new Error(`Shouldn't resolve with invalid mode.`))
            })
            .catch((err) => {
                MockBinding.reset();
                done();
            });
    });
    it('Set polling interval', (done) => {
        const INTERVAL = 100;
        const msk = getMockMSK();
        msk.once('rpc-request', (data) => {
            const objRequest = JSON.parse(data);
            assert.equal(objRequest.method, 'set-interval');
            assert.equal(objRequest.params[0].interval, INTERVAL);
            msk.emit('rpc-response', {
                id: objRequest.id,
                err: null,
                value: null
            });
        });
        msk.connect()
            .then(device => device.setInterval(INTERVAL))
            .then((result) => {
                if(result.err != null) {
                    done(new Error(result.err));
                } else {
                    MockBinding.reset();
                    done()
                }
            })
            .catch(done);
    });
    it('Fail setting invalid polling interval', (done) => {
        const INTERVAL = '100';
        const msk = getMockMSK();
        msk.connect()
            .then(device => device.setInterval(INTERVAL))
            .then((result) => {
                done(new Error(`Shouldn't resolve with invalid interval.`));
            })
            .catch((err) => {
                MockBinding.reset();
                done();
            });
    });
    it('Trigger correct event when get proximity data', (done) => {
        const mockProximity = 127;
        const msk = getMockMSK();
        msk.once('proximity', (proximity) => {
            assert.equal(proximity, mockProximity);
            done();
        });
        msk.connect()
            .then((device) => {
                device.lineReader.emit('line', `{"type": "event", "name": "proximity-data", "detail": {"proximity": ${mockProximity}}}`);
            });
    });
    it('Trigger correct event when get gesture data', (done) => {
        const mockGesture = 'left';
        const msk = getMockMSK();
        msk.once('gesture', (gesture) => {
            assert.equal(gesture, mockGesture);
            done();
        });
        msk.connect()
            .then((device) => {
                device.lineReader.emit('line', `{"type": "event", "name": "gesture", "detail": {"type": "${mockGesture}"}}`);
            });
    });
});
