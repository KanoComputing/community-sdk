const SerialPort = require('serialport');
const MotionSensor = require('./motionsensorkit.js');
const PixelKit = require('./retailpixelkit.js');
const vendorIds = {
    '2341': 'msk',
    '0403': 'rpk'
};
const productIds = {
    '814e': 'msk',
    '6015': 'rpk'
}

class DeviceManager {
    /**
     * Request all the connected Kano devices. It resolves the promise with an array
     * of classes representing the connected devices and ready to use (no need to
     * connect or configure).
     *
     * @return {Promise}
     */
    static listConnectedDevices() {
        return SerialPort.list()
        .then((ports) => {
            let deviceTypes = Object.keys(vendorIds);

            // Filter only ids that exist on the `vendorIds` dictionary
            let serialPorts = ports.filter((port) => {
                if(port.vendorId && port.productId) {
                    let vid = port.vendorId.toLowerCase();
                    let pid = port.productId.toLowerCase();
                    return vendorIds[vid] && productIds[pid];
                }
            });

            let devicesPromise = serialPorts.map((port) => {
                switch(vendorIds[port.vendorId]) {
                    case 'msk':
                        let msk = new MotionSensor({
                            path: port.comName,
                            SerialChannel: this.SerialChannel
                        });
                        return msk.connect();
                        break;
                    case 'rpk':
                        let rpk = new PixelKit({
                            path: port.comName,
                            SerialChannel: this.SerialChannel
                        });
                        return rpk.connect();
                        break;
                    default:
                }
            });
            return Promise.all(devicesPromise);
        });
    }
}

module.exports = DeviceManager
