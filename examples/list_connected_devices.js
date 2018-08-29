/**
This example will list all the available/connected Kano devices and filter it
by its classes.
*/

const DeviceManager = require('../communitysdk').DeviceManager;
const PixelKit = require('../communitysdk').RetailPixelKit;
const MotionSensorKit = require('../communitysdk').MotionSensorKit;

DeviceManager.listConnectedDevices()
.then((devices) => {
    console.log(`Found ${devices.length} connected devices`);
    let availableMotionSensors = devices.filter((device) => {
        return device instanceof MotionSensorKit;
    });
    let availablePixelKits = devices.filter((device) => {
        return device instanceof PixelKit;
    });
    console.log(`Found ${availableMotionSensors.length} available Motion Sensor Kits`);
    console.log(`Found ${availablePixelKits.length} available Pixel Kits`);
});
