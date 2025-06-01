#!/bin/bash
set -e

echo "Updating repository..."

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Stop the services
echo "Stopping services..."
./stop.sh

# Pull latest changes
echo "Pulling latest changes from GitHub..."
git pull

# Activate virtual environment
source venv/bin/activate

# Update dependencies
echo "Updating dependencies..."
pip install -r requirements.txt

# Start the services
echo "Starting services..."
./start.sh

echo "Update completed successfully!" 