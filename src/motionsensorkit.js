const SerialPort = require('serialport');
const createInterface = require('readline').createInterface;
const RPCClient = require('./rpcclient');

class MotionSensorKit extends RPCClient {
    /**
     * Constructor for Motion Sensor class
     *
     * @param {Object} options Options for Motion Sensor class. It should
     *      contain at least a property with `path`.
     */
    constructor(options) {
        if (!options.path) {
            throw new Error('Path is required');
        }
        super();
        if(options.SerialChannel) {
            this.SerialChannel = options.SerialChannel;
        } else {
            this.SerialChannel = SerialPort
        }
        this.port = new this.SerialChannel(options.path, {
            baudRate: 115200,
            autoOpen: false
        });
        this.lineReader = createInterface({
            input: this.port
        });
    }
    /**
     * Opens the serial port and call `bindEvents`
     *
     * @return {Promise}
     */
    connect() {
        return new Promise((resolve, reject) => {
            this.port.on('open', (err) => {
                if (err) {
                    reject(err);
                    return;
                }
                this.bindEvents();
                resolve(this);
            });
            this.port.open();
        });
    }
    /**
     * Binds events from serial port to internal event emitter (bus) and from
     * the event emitter to the serial port.
     */
    bindEvents() {
        // Handles everything the serial port sends.
        this.lineReader.on('line', (d) => {
            try {
                // The data will come as a serialized/stringified json, therefore
                // we must parse it to get it's values.
                let data = JSON.parse(d.toString());
                // Proxy the `data` event to internal event emitter.
                this.emit('data', data);
                // Creates specific events on the internal event emitter based
                // on the `data` properties.
                if(data.type == 'event') {
                    switch (data.name) {
                        case 'proximity-data':
                            this.emit('proximity', data.detail.proximity);
                            break;
                        case 'gesture':
                            this.emit('gesture', data.detail.type);
                            break;
                        case 'error':
                            this.emit('error-message', data.detail.msg);
                            break;
                        default:
                    }
                }
            } catch(e) {
                throw e
            }
        });

        // Writes/sends something to the serial port
        this.on('rpc-request', (data) => {
            this.port.write(Buffer.from(data));
        });
    }
    /**
     * Sends an RPC request to set the MSK mode.
     *
     * @param {String} mode Mode to set on the MSK. It could be either
     *      `proximity` or `gesture`.
     * @return {Promise}
     */
    setMode(mode) {
        if (mode !== 'proximity' && mode !== 'gesture') {
            throw new Error('Motion sensor mode can only be set to `gesture` or `proximity`.');
        }
        return this.rpcRequest('set-mode', [{mode: mode}]);
    }
    /**
     * Sends an RPC request to set the MSK data polling interval.
     *
     * @param {Number} inteval How often should the MSK ask the hardware sensor
     *      for information (in milliseconds).
     * @return {Promise}
     */
    setInterval(interval) {
        if (typeof interval != 'number') {
            throw new Error('Motion sensor interval must be a number.');
        }
        return this.rpcRequest('set-interval', [{interval: parseInt(interval)}]);
    }
}

module.exports = MotionSensorKit
