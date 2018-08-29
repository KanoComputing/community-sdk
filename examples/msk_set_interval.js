/**
This example will set the Motion Sensor Kit to poll data every 500 milliseconds.
*/
const DeviceManager = require('../communitysdk').DeviceManager;
const MotionSensorKit = require('../communitysdk').MotionSensorKit;

DeviceManager.listConnectedDevices()
.then((devices) => {
    // Filter devices to find a Motion Sensor Kit
    let msk = devices.find((device) => {
        return device instanceof MotionSensorKit;
    });
    if(!msk) {
        console.log('No Motion Sensor Kit was found :(');
    } else {
        console.log('Motion Sensor Kit found!');
        // Set mode to proximity
        msk.setMode('proximity')
            .then(() => {
                // Set polling interval to 500 milliseconds
                return msk.setInterval(500);
            })
            .then(() => {
                // Prints proximity data
                msk.on('proximity', (p) => {
                    console.log('Proximity value:', p);
                });
            });
    }
});
