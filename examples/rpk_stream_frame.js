const DeviceManager = require('../src/manager');
const PixelKit = require('../src/retailpixelkit');

DeviceManager.listConnectedDevices()
.then((devices) => {
    if(devices.length && devices[0] instanceof PixelKit) {
        const rpk = devices[0];
        setInterval(() => {
            const hexColors = [];
            for(let i = 0; i < 128; i++) {
                hexColors.push('#'+(Math.random()*0xFFFFFF<<0).toString(16));
            }
            rpk.streamFrame(hexColors)
                .then(data => console.log('frame streamed'))
                .catch(err => console.log('error', err));
        }, 500);
    }
});
