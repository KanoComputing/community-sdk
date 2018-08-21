const DeviceManager = require('../src/manager');
const PixelKit = require('../src/retailpixelkit');

DeviceManager.listConnectedDevices()
.then((devices) => {
    if(devices.length && devices[0] instanceof PixelKit) {
        const rpk = devices[0];
        rpk.connectToWifi('NETWORK', 'PASSWORD')
            .then((data) => {
                console.log('connected to wifi', data)
            })
            .catch((err) => {
                console.log(`couldn't connect`, err)
            });
    }
});
