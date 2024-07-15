#!/bin/bash

# Get the process IDs of all running node processes
pids=$(pgrep node)

if [ -z "$pids" ]; then
  echo "No node processes found."
else
  echo "Stopping node processes: $pids"
  for pid in $pids; do
    echo "Stopping process ID $pid"
    kill $pid
  done
fi
