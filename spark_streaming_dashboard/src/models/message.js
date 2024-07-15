const mongoose = require('mongoose');
const { Schema } = mongoose;

const messageSchema = new Schema({
    id: { type: Number, required: true },
    text: { type: String, required: true },
    user: { type: String, required: true },
    is_hateful: { type: Number, required: true }
});

const Message = mongoose.model('Message', messageSchema);

module.exports = Message;
