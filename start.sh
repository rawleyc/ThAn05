#!/bin/bash

# Exit on error
set -e

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Check if screen is installed
if ! command -v screen &> /dev/null; then
    echo "Installing screen..."
    sudo apt-get update
    sudo apt-get install -y screen
fi

# Check if Python virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Create files directory if it doesn't exist
mkdir -p files

# Kill any existing screen sessions
screen -X -S telegram-bot quit 2>/dev/null || true
screen -X -S file-server quit 2>/dev/null || true

# Start the bot in a screen session
echo "Starting Telegram Bot..."
screen -dmS telegram-bot bash -c "cd '$SCRIPT_DIR' && source venv/bin/activate && python3 bot.py; exec bash"

# Start the file server in a screen session
echo "Starting File Server..."
screen -dmS file-server bash -c "cd '$SCRIPT_DIR' && source venv/bin/activate && gunicorn -w 4 -b 0.0.0.0:8080 server:app; exec bash"

# Wait a moment for sessions to start
sleep 2

# Check if sessions are running
if screen -ls | grep -q "telegram-bot"; then
    echo "✅ Telegram Bot started successfully"
else
    echo "❌ Failed to start Telegram Bot"
    exit 1
fi

if screen -ls | grep -q "file-server"; then
    echo "✅ File Server started successfully"
else
    echo "❌ Failed to start File Server"
    exit 1
fi

echo -e "\nTo view the bot logs: screen -r telegram-bot"
echo "To view the server logs: screen -r file-server"
echo "To detach from a screen session: Press Ctrl+A, then D" 