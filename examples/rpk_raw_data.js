const DeviceManager = require('../src/manager');
const PixelKit = require('../src/retailpixelkit');

DeviceManager.listConnectedDevices()
.then((devices) => {
    if(devices.length && devices[0] instanceof PixelKit) {
        const rpk = devices[0];
        rpk.on('data', (data) => {
            console.log('data', data);
        });
    }
});
