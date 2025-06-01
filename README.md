# Telegram File Sharing Bot

A Telegram bot that allows users to share files and get direct download links. The bot runs on an Ubuntu server and uses screen sessions for process management.

## Features

- Supports various file types:
  - Images (JPEG, PNG, GIF, WebP)
  - Videos (MP4, MOV, AVI)
  - Audio files (MP3, OGG, WAV)
  - Documents (PDF, DOC, DOCX)
  - Archives (RAR, ZIP)
  - Text files (TXT, CSV)
- File size limit: 5GB
- Direct download links via HTTP
- Automatic file cleanup
- Screen session management
- Easy update process

## Prerequisites

- Ubuntu server
- Python 3.8 or higher
- Git
- Screen

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/ThAn05.git
cd ThAn05
```

2. Set up environment variables in `.bashrc`:
```bash
echo '
# Telegram Bot Environment Variables
export BOT_TOKEN=your_bot_token_here
export BASE_URL=http://your-domain:8080
export FILES_DIR=files
' >> ~/.bashrc

source ~/.bashrc
```

3. Make scripts executable:
```bash
chmod +x start.sh stop.sh update.sh
```

4. Start the services:
```bash
./start.sh
```

## Usage

### Bot Commands
- `/start` - Start the bot
- `/help` - Show help message

### File Sharing
1. Send any supported file to the bot
2. The bot will provide a direct download link
3. Files are automatically cleaned up after 24 hours

### Server Management

#### Start Services
```bash
./start.sh
```
This will:
- Create Python virtual environment if needed
- Install dependencies
- Start bot and server in screen sessions

#### Stop Services
```bash
./stop.sh
```
This will:
- Stop all screen sessions
- Kill any remaining processes
- Free port 8080

#### Update Bot
```bash
./update.sh
```
This will:
- Stop services
- Pull latest changes from GitHub
- Update dependencies
- Restart services

### Viewing Logs
- Bot logs: `screen -r telegram-bot`
- Server logs: `screen -r file-server`
- Detach from screen: Press `Ctrl+A` then `D`

## Environment Variables

- `BOT_TOKEN`: Your Telegram bot token from @BotFather
- `BASE_URL`: Your server's domain or IP with port (e.g., http://your-domain:8080)
- `FILES_DIR`: Directory to store uploaded files (default: 'files')

## File Types Support

### Images
- JPEG
- PNG
- GIF
- WebP

### Videos
- MP4
- MOV
- AVI

### Audio
- MP3
- OGG
- WAV

### Documents
- PDF
- DOC
- DOCX

### Archives
- RAR
- ZIP

### Text
- TXT
- CSV

## Security Features

- File type validation
- File size limits
- Automatic file cleanup
- CORS support
- Security headers

## Troubleshooting

### Port 8080 in Use
If port 8080 is already in use:
```bash
./stop.sh
```
This will free the port and kill any lingering processes.

### Screen Sessions
To list all screen sessions:
```bash
screen -ls
```

To kill all screen sessions:
```bash
pkill screen
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.