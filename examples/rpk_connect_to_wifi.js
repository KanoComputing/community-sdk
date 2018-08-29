/**
This example will connect your Pixel Kit to a wifi network.
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
        console.log('Connecting to wifi...');
        rpk.connectToWifi('NETWORK', 'PASSWORD')
        .then((data) => {
            console.log('Connected to wifi network', data);
        })
        .catch((err) => {
            console.log(`Couldn't connect to wifi network`, err);
        });
    }
});
