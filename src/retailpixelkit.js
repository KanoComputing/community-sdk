const SerialPort = require('serialport');
const WebSocket = require('ws');
const createInterface = require('readline').createInterface;
const RPCClient = require('./rpcclient');

class RetailPixelKit extends RPCClient {
    /**
     * Constructor for Motion Sensor class
     *
     * @param {Object} options Options for Pixek Kit class. It should
     *      contain at least a property with `path`.
     */
    constructor(options) {
        if (!options || (!options.path && !options.ip)) {
            throw new Error('Path or ip address are required');
        }
        super();
        if (options.path) {
            this.port = new SerialPort(options.path, {
                baudRate: 115200,
                autoOpen: false
            });
            this.lineReader = createInterface({
                input: this.port
            });
        } else if (options.ip) {
            this.ip = options.ip;
        }
    }

    parseEvents(d) {
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
                    case 'button-down':
                        this.emit('button-down', data.detail['button-id']);
                        break;
                    case 'button-up':
                        this.emit('button-up', data.detail['button-id']);
                        break;
                    case 'mode-change':
                        this.emit('dial', data.detail['mode-id']);
                        break;
                    case 'error':
                        this.emit('error-message', data.detail.msg);
                        break;
                    default:
                }
            }
        } catch (e) {
            this.emit('error-message', e.message)
        }
    }
    bindSerialEvents() {
        // Handles everything the serial port sends.
        // this.port.on('data', (d) => {
        this.lineReader.on('line', (d) => this.parseEvents(d));
        // Writes/sends something to the serial port
        this.on('rpc-request', (data) => {
            this.port.write(Buffer.from(data));
        });
    }
    bindWebSocketEvents() {
        this.ws.on('message', (d) => this.parseEvents(d));
        // Writes/sends something to websocket
        this.on('rpc-request', (data) => {
            this.ws.send(Buffer.from(data))
        });
    }
    connectToSerial() {
        return new Promise((resolve, reject) => {
            this.port.on('open', (err) => {
                if (err) {
                    reject(err);
                    return;
                }
                this.bindSerialEvents();
                resolve(this);
            });
            this.port.open();
        });
    }
    connectToWebSocket() {
        return new Promise((resolve, reject) => {
            this.ws = new WebSocket(`ws://${this.ip}:9998`);
            this.ws.on('open', (err) => {
                if (err) {
                    reject(err);
                    return;
                }
                this.bindWebSocketEvents();
                resolve(this);
            });
            // this.ws.open();
        });
    }
    /**
     * Binds events from serial port to internal event emitter (bus) and from
     * the event emitter to the serial port.
     */
    bindEvents() {
        if (this.port) {
            this.bindSerialEvents();
        } else if (this.ip) {
            this.bindWebSocketEvents();
        } else {
            console.log('No connection found');
        }
    }
    /**
     * Opens the serial port and call `bindEvents`
     *
     * @return {Promise}
     */
    connect() {
        if (this.port) {
            return this.connectToSerial();
        } else if (this.ip) {
            return this.connectToWebSocket();
        } else {
            console.log('No connection found');
            return Promise.reject();
        }
    }

    hexToBase64Colors(element) {
        let frameBuffer = new Buffer(element.length * 2, 0);

        element.forEach((color, index) => {
            let colorBin = new Buffer(2),
                rgb888,
                rgb565;

            if (typeof color === "string" && color.length === 7 && /#[0-9a-f]{6}/i.test(color)) {
                rgb888 = parseInt(color.substring(1, 7), 16);
                //                blue                 green                  red
                rgb565 = (rgb888 & 0xF8) >> 3 | (rgb888 & 0xFC00) >> 5 | (rgb888 & 0xF80000) >> 8;

                colorBin.writeUInt16BE(rgb565, 0);
            } else {
                // If the color is invalid, write black
                colorBin.writeUInt16BE(0x0000, 0);
            }

            colorBin.copy(frameBuffer, index * 2);
        });
        return frameBuffer.toString('base64');
    }
    // frame must be an array with 128 hexadecimal colors prefixed with a `#`
    streamFrame(frame) {
        let encodedFrame = this.hexToBase64Colors(frame);
        return this.rpcRequest('lightboard:on', [{ map: encodedFrame }]);
    }
    getBatteryStatus() {
        return this.rpcRequest('battery-status', []);
    }
    getWifiStatus() {
        return this.rpcRequest('wifi-status', []);
    }
    scanWifi() {
        return this.rpcRequest('wifi-scan', []);
    }
    connectToWifi(ssid, password) {
        return this.rpcRequest('wifi-connect', [ssid, password]);
    }
}

module.exports = RetailPixelKit
