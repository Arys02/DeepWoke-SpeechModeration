const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
const Message = require('../models/message');  // Adjust the path to your model

const app = express();
const port = 3002;

app.use(bodyParser.json({ limit: '50mb', type: 'application/json' }));
app.use(bodyParser.urlencoded({ limit: '50mb', extended: true, parameterLimit: 50000 }));

// Middleware to set UTF-8 charset for responses
app.use((req, res, next) => {
    res.setHeader('Content-Type', 'application/json; charset=UTF-8');
    next();
});

mongoose.connect('mongodb://127.0.0.1:27017/messages', { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => console.log('Connected to MongoDB'))
    .catch((err) => {
        console.error('Failed to connect to MongoDB', err);
        process.exit(1);
    });

app.post('/detect', (req, res) => {
    const messages = req.body;
    const responses = messages.map((message) => {
        const isHateful = Math.random() < 0.2 ? 1 : 0;
        return {

            id: message.id,
            is_hateful: isHateful,
        };
    });
    res.json(responses);
});

app.post('/messages', async (req, res) => {
    const messages = req.body; // Expecting an array of messages

    console.log("Received messages:");

    try {
        //await Message.insertMany(messages.message.messages);
        res.json({ message: 'Messages posted successfully' });
        console.log("nothing happened, insert many is commented");
    } catch (error) {
        console.error('Error posting messages:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

app.get('/messages', async (req, res) => {
    const { user, is_hateful } = req.query;

    const query = {};
    if (user) query.user = user;
    if (is_hateful !== undefined) query.is_hateful = is_hateful === 'true';

    try {
        const messages = await Message.find(query);
        res.json(messages);
    } catch (error) {
        console.error('Error fetching messages:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

app.listen(port, () => {
    console.log(`Hate messages API running on http://localhost:${port}`);
});
