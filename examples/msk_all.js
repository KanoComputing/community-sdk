/**
This example will toggle between proximity and gesture mode every 5 seconds,
print both proximity and gestures when detected and set the polling interval
to 500 ms.
*/
const DeviceManager = require('./src/manager');
const MotionSensor = require('./src/motionsensorkit');
let manager = new DeviceManager();

// Set mode to proximity and schedule to change to gesture after 5 seconds
const setProximity = (device) => {
    console.log('setting mode to proximity');
    return device.setMode('proximity')
        .then(() => {
            setTimeout(() => {
                setGesture(device);
            }, 5000);
        });
}
// Set mode to gesture and schedule to change to proximity after 5 seconds
const setGesture = (device) => {
    console.log('setting mode to gesture');
    return device.setMode('gesture')
        .then(() => {
            setTimeout(() => {
                setProximity(device);
            }, 5000);
        });
}

manager.listConnectedDevices()
.then((devices) => {
    // Check if there are any Kano devices connected
    if(devices.length) {
        // Make sure it's a Motion Sensor
        if(devices[0] instanceof MotionSensor) {
            const msk = devices[0];
            // Change polling time to 500 ms
            msk.setInterval(500);
            // Prints proximity data
            msk.on('proximity', (p) => {
                console.log('proximity', p);
            });
            // Prints gesture data
            msk.on('gesture', (g) => {
                console.log('gesture', g);
            });
            // Start toggling between proximity and gesture
            setProximity(msk);
        }
    }
});
