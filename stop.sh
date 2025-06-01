#!/bin/bash

# Exit on error
set -e

# Function to safely stop a screen session
stop_screen_session() {
    local session_name=$1
    if screen -ls | grep -q "$session_name"; then
        echo "Stopping $session_name..."
        screen -X -S "$session_name" quit || true
        sleep 1
        if ! screen -ls | grep -q "$session_name"; then
            echo "✅ $session_name stopped successfully"
        else
            echo "❌ Failed to stop $session_name"
            return 1
        fi
    else
        echo "ℹ️ $session_name is not running"
    fi
}

# Stop the bot screen session
stop_screen_session "telegram-bot"

# Stop the file server screen session
stop_screen_session "file-server"

echo "All services stopped." 