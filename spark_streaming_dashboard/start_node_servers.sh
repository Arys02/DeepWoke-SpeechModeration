#!/bin/bash

# Start the first service
nohup npm run dev > dev.log 2>&1 &

# Start the second service with nodemon
nohup nodemon server.js > server.log 2>&1 &

# Start the third service with nodemon in the src/api directory
cd src/api
nohup nodemon hate_speech_api.js > ../hate_speech_api.log 2>&1 &
cd ../..

echo "All services started"