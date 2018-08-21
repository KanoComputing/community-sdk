const EventEmitter = require('events');
const uuid = require('uuid');

class RPCClient extends EventEmitter {
    constructor() {
        super();
        // When the data is an `rpc-response`, creates a custom event on
        // internal emitter
        this.on('data', (data) => {
            if(data.type == 'rpc-response') {
                this.emit('rpc-response', data);
            }
        });
    }

    /**
     * Sends an RPC request to device calling for a `method` passing `params`.
     *
     * @param {String} method Which RPC method to call on the board.
     * @param {Array} params Parameters for the current method.
     * @return {Promise}
     */
    rpcRequest(method, params) {
        let requestObject = this.getRPCRequestObject(method, params);
        return this.rpcPromise(requestObject);
    }

    /**
     * Creates an JSON object with an RPC request
     *
     * @param {String} method RPC method being requested
     * @param {Array} params Array of parameters to send over the RPC request
     * @return {Object}
     */
    getRPCRequestObject(method, params) {
        return {
            type: "rpc-request",
            id: uuid.v4(),
            method: method,
            params: params
        }
    }

    /**
     * Creates a stringified JSON object with an RPC request
     *
     * @param {String} method RPC method being requested
     * @param {Array} params Array of parameters to send over the RPC request
     * @return {String}
     */
    getRPCRequestString (method, params) {
        return JSON.stringify(this.getRPCRequestObject(method, params));
    }

    /**
     * Creates a promise of a RPC request that resolves when the bus emits an RPC
     * response that matches the `id` of the sent request.
     *
     * @param {Object} requestObject JSON object with the RPC request
     * @return {Promise}
     */
    rpcPromise(requestObject) {
        return new Promise((resolve, reject) => {
            let rpcResponseHandler = (data) => {
                if(data.id == requestObject.id) {
                    this.removeListener('rpc-response', rpcResponseHandler);
                    if (data.err) {
                        this.emit('error-message', data.err);
                        reject(new Error(data.err));
                        return;
                    } else if (data.name === 'error') {
                        this.emit('error-message', data.detail.msg);
                        reject(new Error(data.detail.msg));
                        return;
                    }
                    resolve(data);
                }
            };
            this.on('rpc-response', rpcResponseHandler);
            this.emit('rpc-request', JSON.stringify(requestObject)+'\r\n');
        });
    }
};

module.exports = RPCClient;
