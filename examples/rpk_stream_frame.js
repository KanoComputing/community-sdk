/**
This example will stream a series of single color "frames" to Pixel Kit.
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
        /*
        A frame is an array of 128 hexadecimal colors prefixed with `#`.
        We'll create a single color frame (all the pixels with the same
        color) to stream to Pixel Kit.
        */
        let frame = [];
        for(let i = 0; i < 128; i++) {
            frame.push('#ffff00'); // Yellow frame!
        }
        /*
        We will send a frame every 100 milliseconds to Pixel Kit (10 frames
        per second). It's important to keep sending frames to the Pixel Kit,
        otherwise it will go back to the mode it was before.
        */
        console.log('Streaming frame.');
        setInterval(() => {
            rpk.streamFrame(frame)
                .catch((error) => {
                    console.log('Problem streaming frame', error);
                });
        }, 100);
    }
});
