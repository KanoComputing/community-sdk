/**
This example will connect to your Pixel Kit over wifi. For that you need to
first connect your Pixel Kit to the same wifi network as your computer is
connected. Then you will need to get the wifi status to copy your Pixel Kit
ip address.
*/

const PixelKit = require('../communitysdk').RetailPixelKit;

/*
Connect your Pixel Kit to the same wifi as your computer and get its
ip on the connection response or via `getWifiStatus()` method.
*/
let rpk = new PixelKit({ip: '192.168.0.95'});

rpk.connect()
    .then((device) => {
        console.log('Connected to pixel kit wirelessly!');
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
        /*
        Create a frame with 128 random hexadecimal colors and stream it every
        500 milliseconds.
        */
        setInterval(() => {
            const frame = [];
            for(let i = 0; i < 128; i++) {
                frame.push('#'+(Math.random()*0xFFFFFF<<0).toString(16));
            }
            rpk.streamFrame(frame)
                .catch(err => console.log('Error streaming frame', err));
        }, 500);
    })
