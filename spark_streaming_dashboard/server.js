const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const next = require('next');
const { createProxyMiddleware } = require('http-proxy-middleware');
const cors = require('cors');
const debug = require('debug')('myapp:server');
const axios = require('axios');
const url = require('url');

const app = next({ dev: true, dir: './src' });
const handle = app.getRequestHandler();

app.prepare().then(() => {
    const server = express();

    server.use(cors({
        origin: true,
        methods: ["GET", "POST", "OPTIONS", "PUT", "PATCH", "DELETE"],
        credentials: true
    }));

    // Proxy WebSocket connections for webpack HMR
    server.use('/pa_2024_online_version/spark_streaming_dashboard/_next/webpack-hmr', createProxyMiddleware({
        target: 'ws://localhost:3000',
        ws: true,
        changeOrigin: true,
        logLevel: 'debug'
    }));

    // Setup WebSocket server for other usage
    const httpServer = http.createServer(server);
    const wss = new WebSocket.Server({ server: httpServer });

    wss.on('connection', (ws, req) => {
        const parameters = url.parse(req.url, true);
        const clientType = parameters.query.clientType;

        console.log(`New client connected: ${clientType}`);

        if (clientType === 'spark') {
            sparkClient = ws;
            console.log('Spark client connected');
        }

        ws.on('message', async (message) => {
            debug('Received message from client:', message);
            console.log('Received message from client:', message);

            // Parse the received message
            let parsedMessage;
            try {
                parsedMessage = JSON.parse(message);
            } catch (err) {
                console.error('Failed to parse message. Error:', err);
                return;
            }

            if (parsedMessage.type == "inbound") {
                console.log(JSON.stringify(parsedMessage));
                console.log("sending to spark");
                sparkClient.send(JSON.stringify(parsedMessage));
            } else {
                try {
                    await axios.post('http://localhost:3002/messages', { message: parsedMessage });
                    console.log('Message sent to hatespeech_api');
                } catch (err) {
                    console.error('Failed to send message to hatespeech_api. Error:', err);
                }

                // Broadcast message to all clients
                wss.clients.forEach((client) => {
                    if (client.readyState === WebSocket.OPEN) {
                        client.send(message);
                    }
                });
            }

        });

        ws.on('close', () => {
            debug('Client disconnected');
            console.log('Client disconnected');
        });

        ws.on('error', (error) => {
            debug('WebSocket error:', error);
            console.error('WebSocket error:', error);
        });
    });

    server.all('*', (req, res) => {
        debug('Handling request for %s', req.url);
        return handle(req, res);
    });

    const PORT = process.env.PORT || 3001;
    httpServer.listen(PORT, (err) => {
        if (err) throw err;
        console.log(`> Ready on http://localhost:${PORT}`);
    });
});
