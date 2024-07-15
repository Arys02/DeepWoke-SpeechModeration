#!/bin/bash

# Check if the screen session name file exists
if [ -f spark_screen_name.txt ]; then
    # Extract the screen session name
    screen_name=$(cat spark_screen_name.txt)

    # Check if the screen session is running
    if screen -list | grep -q "$screen_name"; then
        # Terminate the screen session
        screen -S "$screen_name" -X quit
        rm spark_screen_name.txt
        echo "Spark job stopped."
    else
        echo "No Spark job running with the screen session name: $screen_name."
    fi
else
    echo "No Spark job running."
fi
