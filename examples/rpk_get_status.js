const DeviceManager = require('../src/manager');
const PixelKit = require('../src/retailpixelkit');

DeviceManager.listConnectedDevices()
.then((devices) => {
    if(devices.length && devices[0] instanceof PixelKit) {
        const rpk = devices[0];
        rpk.getBatteryStatus().then((data) => {
            console.log('battery status', data)
        })
        rpk.getWifiStatus().then((data) => {
            console.log('wifi status', data)
        })
        rpk.scanWifi().then((data) => {
            console.log('scan wifi', data)
        })
    }
});
