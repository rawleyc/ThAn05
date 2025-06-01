#!/bin/bash

# Check if screen is installed
if ! command -v screen &> /dev/null; then
    echo "Installing screen..."
    sudo apt-get update
    sudo apt-get install -y screen
fi

# Create files directory if it doesn't exist
mkdir -p files

# Activate virtual environment and start the bot
screen -dmS telegram-bot bash -c '
    source venv/bin/activate
    python3 bot.py
'

# Activate virtual environment and start the file server
screen -dmS file-server bash -c '
    source venv/bin/activate
    gunicorn -w 4 -b 0.0.0.0:8080 server:app
'

echo "Services started in screen sessions."
echo "To view the bot logs: screen -r telegram-bot"
echo "To view the server logs: screen -r file-server"
echo "To detach from a screen session: Press Ctrl+A, then D" 