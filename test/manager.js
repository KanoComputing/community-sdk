const assert = require('assert');
const MockBinding = require('./util/mockbinding');
const DeviceManager = require('../src/manager');
const MotionSensor = require('../src/motionsensorkit');
const PixelKit = require('../src/retailpixelkit');

let manager = new DeviceManager(MockBinding);

describe('Available devices', () => {
    it('Should not list devices without  pid and vid', (done) => {
        MockBinding.createPort('WRONG_DEVICE', {
            vendorId: undefined,
            productId: undefined
        });
        manager.listConnectedDevices()
            .then((devices) => {
                assert.equal(devices.length, 0);
                MockBinding.reset();
                done();
            })
            .catch(done);
    });
    it('Should not list devices with non-kano pid and vid', (done) => {
        MockBinding.createPort('WRONG_DEVICE', {
            vendorId: 'wrong',
            productId: 'wrong'
        });
        manager.listConnectedDevices()
            .then((devices) => {
                assert.equal(devices.length, 0);
                MockBinding.reset();
                done();
            })
            .catch(done);
    });
    it('Should list devices with the correct pid and vid', (done) => {
        MockBinding.createPort('MOTION_SENSOR_KIT', {
            vendorId: '2341',
            productId: '814e'
        });
        MockBinding.createPort('RETAIL_PIXEL_KIT', {
            vendorId: '0403',
            productId: '6015'
        });
        manager.listConnectedDevices()
            .then((devices) => {
                assert.equal(devices.length, 2);
                MockBinding.reset();
                done();
            })
            .catch(done);
    });
    it('Should resolve list promise with the device instances', (done) => {
        MockBinding.createPort('MOTION_SENSOR_KIT', {
            vendorId: '2341',
            productId: '814e'
        });
        MockBinding.createPort('RETAIL_PIXEL_KIT', {
            vendorId: '0403',
            productId: '6015'
        });
        manager.listConnectedDevices()
            .then((devices) => {
                assert.equal(devices.length, 2);
                assert.ok(devices[0] instanceof MotionSensor);
                assert.ok(devices[1] instanceof PixelKit);
                MockBinding.reset();
                done();
            })
            .catch(done);
    });
});
