#!/bin/bash

# Exit on error
set -e

echo "Stopping services..."

# Function to stop a screen session
stop_screen_session() {
    local session_name=$1
    if screen -list | grep -q "$session_name"; then
        echo "Stopping $session_name..."
        screen -S "$session_name" -X quit
        echo "$session_name stopped successfully"
    else
        echo "$session_name is not running"
    fi
}

# Stop screen sessions
stop_screen_session "telegram-bot"
stop_screen_session "file-server"

# Kill any remaining gunicorn processes
echo "Cleaning up gunicorn processes..."
pkill -f gunicorn || true

# Kill any process using port 8080
echo "Freeing port 8080..."
fuser -k 8080/tcp || true

# Verify port is free
if lsof -i :8080 > /dev/null 2>&1; then
    echo "Warning: Port 8080 is still in use. Attempting force kill..."
    sudo fuser -k -9 8080/tcp || true
fi

echo "Services stopped successfully" 