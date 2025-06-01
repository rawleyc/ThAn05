#!/bin/bash

# Function to safely stop a screen session
stop_screen_session() {
    local session_name=$1
    if screen -ls | grep -q "$session_name"; then
        screen -X -S "$session_name" quit
        echo "Stopped $session_name session"
    else
        echo "$session_name session not found"
    fi
}

# Stop the bot screen session
stop_screen_session "telegram-bot"

# Stop the file server screen session
stop_screen_session "file-server"

echo "All services stopped." 