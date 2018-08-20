const assert = require('assert');
const RPCClient = require('../src/rpcclient');

describe('Exchange data with an RPC server', () => {
    it('Should generate a valid RPC request object', (done) => {
        const client = new RPCClient();
        const method = 'methodName';
        const params = ['param1'];
        const request = client.getRPCRequestObject(method, params);
        assert.ok(request.id)
        assert.equal(request.type, 'rpc-request');
        assert.equal(request.method, method);
        assert.deepEqual(request.params, params);
        done();
    });
    it('Should generate a valid RPC request string', (done) => {
        const client = new RPCClient();
        const method = 'methodName';
        const params = ['param1'];
        const strRequest = client.getRPCRequestString(method, params);
        assert.equal(strRequest.indexOf(' '), -1);
        const objRequest = JSON.parse(strRequest);
        assert.ok(objRequest.id)
        assert.equal(objRequest.type, 'rpc-request');
        assert.equal(objRequest.method, method);
        assert.deepEqual(objRequest.params, params);
        done();
    });
    it('Should emit an `rpc-request` event with the correct data when request is made', (done) => {
        const client = new RPCClient();
        const method = 'methodName';
        const params = ['param1'];
        const strRequest = client.getRPCRequestString(method, params);
        client.once('rpc-request', (data) => {
            const objRequest = JSON.parse(data);
            assert.ok(objRequest.id)
            assert.equal(objRequest.type, 'rpc-request');
            assert.equal(objRequest.method, method);
            assert.deepEqual(objRequest.params, params);
            done();
        });
        let promise = client.rpcRequest(method, params);
    });
    it('Should emit an `rpc-response` event when receiving a `data` event with an `rpc-request`', (done) => {
        const client = new RPCClient();
        const serverData = {
            type: 'rpc-response',
            id: '188762c8-b0e4-4d11-afe9-400a4a8668a7',
            err: null,
            value: null
        };
        client.once('rpc-response', (data) => {
            assert.deepEqual(data, serverData);
            done();
        });
        client.emit('data', serverData);
    });
    it('Should resolve `rpcPromise` when an `rpc-response` event is emitted for the correct request (matching ids)', (done) => {
        const client = new RPCClient();
        const method = 'methodName';
        const params = ['param1'];
        const objRequest = client.getRPCRequestObject(method, params);

        client.once('rpc-request', (data) => {
            const serverData = {
                type: 'rpc-response',
                id: objRequest.id,
                err: null,
                value: null
            };
            client.emit('data', serverData);
        });
        client.rpcPromise(objRequest)
            .then(data => done());
    });
    it('Should resolve `rpcRequest` when an `rpc-response` event is emitted for the correct request (matching ids)', (done) => {
        const client = new RPCClient();
        const method = 'methodName';
        const params = ['param1'];

        client.once('rpc-request', (data) => {
            const objRequest = JSON.parse(data);
            const serverData = {
                type: 'rpc-response',
                id: objRequest.id,
                err: null,
                value: null
            };
            client.emit('data', serverData);
        });
        client.rpcRequest(method, params)
            .then(data => done());
    });
});
