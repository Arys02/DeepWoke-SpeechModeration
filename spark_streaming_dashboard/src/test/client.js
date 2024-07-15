const socket = require('socket.io-client')('http://172.22.134.31:3001', {
    rejectUnauthorized: false // WARN: please do not do this in production
});

socket.on('connect', () => {
    console.log('Successfully connected to the server');

    // Listen for messages from the server
    socket.on('FromAPI', (data) => {
        console.log('Received data from server:', data);
    });

    // Handle disconnection
    socket.on('disconnect', () => {
        console.log('Disconnected from the server');
    });

    // Emit some data to the server
    socket.emit('update', { message: 'Hello from client' });
});

socket.on('connect_error', (error) => {
    console.error('Connection error:', error);
});
