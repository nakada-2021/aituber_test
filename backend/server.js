
// backend/server.js

const WebSocket = require('ws');
const wss = new WebSocket.Server({ port: 8000 });

wss.on('connection', ws => {
    ws.on('message', message => {
        console.log('Received:', message);
    });
});
