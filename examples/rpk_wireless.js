

const PixelKit = require('../src/retailpixelkit');

// Connect your Pixel Kit to the same wifi as your computer and get its
// ip on the connection response or via `getWifiStatus()` method.
const rpk = new PixelKit({ip: '192.168.0.2'});
rpk.connect()
    .then((device) => {
        console.log('Connected to pixel kit wirelessly');
        // From now on you can use all Pixel Kit features without cables!
        device.on('button-down', (button) => {
            console.log(button, 'down');
        });
        device.on('dial', (id) => {
            console.log('dial changed to', id);
        });
        rpk.getBatteryStatus().then((data) => {
            console.log('battery status', data);
        });
        setInterval(() => {
            const hexColors = [];
            for(let i = 0; i < 128; i++) {
                hexColors.push('#'+(Math.random()*0xFFFFFF<<0).toString(16));
            }
            rpk.streamFrame(hexColors)
                .catch(err => console.log('error', err));
        }, 500)
    })
