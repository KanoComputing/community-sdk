/**
This example will scan for available networks, get battery and wifi status from
the Pixel Kit.
*/
const DeviceManager = require('../communitysdk').DeviceManager;
const PixelKit = require('../communitysdk').RetailPixelKit;

DeviceManager.listConnectedDevices()
.then((devices) => {
    // Filter devices to find a Motion Sensor Kit
    let rpk = devices.find((device) => {
        return device instanceof PixelKit;
    });
    if(!rpk) {
        console.log('No Pixel Kit was found :(');
    } else {
        console.log('Pixel Kit found!');
        rpk.scanWifi()
        .then((data) => {
            console.log('Available networks:');
            console.log(data);
        });
        rpk.getBatteryStatus()
        .then((data) => {
            console.log('Battery status:');
            console.log(data);
        });
        rpk.getWifiStatus()
        .then((data) => {
            console.log('Wifi status:');
            console.log(data);
        });
    }
});
