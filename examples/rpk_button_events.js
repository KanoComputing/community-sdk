/**
This example will show how to handle button and dial events triggered by
Pixel Kit.
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
        console.log('Press the buttons and turn the dial mode on your Pixel Kit!')
        rpk.on('button-down', (buttonId) => {
            console.log(`Button ${buttonId} pressed`);
        });
        rpk.on('button-up', (buttonId) => {
            console.log(`Button ${buttonId} released`);
        });
        rpk.on('dial', (modeId) => {
            console.log(`Dial turned to ${modeId}`);
        });
    }
});
