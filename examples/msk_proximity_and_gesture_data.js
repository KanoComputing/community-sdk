/**
This example will switch to `gesture` mode when you move your hand close to the
Motion Sensor Kit and will switch back to `proximity` mode when it recognizes
the gesture "up".
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
        msk.setMode('proximity')
            .then(() => {
                console.log('Move your hand close to it to switch to `gesture` mode.')
            });
        // Prints proximity data
        msk.on('proximity', (p) => {
            // Avoid printing `0` all the time
            if(p > 0) {
                console.log('Proximity value:', p)
            }
            if(p > 250) {
                console.log('Setting mode to `gesture`.')
                msk.setMode('gesture')
                    .then(() => {
                        console.log('Swipe your hand `up` to switch back to `proximity` mode.')
                    });
            }
        });
        // Prints gesture data
        msk.on('gesture', (g) => {
            console.log('Gesture:', g);
            if(g == 'up') {
                console.log('Setting mode to `proximity`.');
                msk.setMode('proximity')
                    .then(() => {
                        console.log('Move your hand close to it to switch to `gesture` mode.')
                    });
            }
        });
    }
});
