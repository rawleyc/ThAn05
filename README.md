# Telegram File Sharing Bot

A fully functional Telegram bot that allows users to share files and get direct download links. The bot runs on an Ubuntu server with Nginx as a reverse proxy and uses screen sessions for process management.

## Features

- ✅ Supports various file types:
  - Images (JPEG, PNG, GIF, WebP)
  - Videos (MP4, MOV, AVI)
  - Audio files (MP3, OGG, WAV)
  - Documents (PDF, DOC, DOCX)
  - Archives (RAR, ZIP)
  - Text files (TXT, CSV)
- ✅ File size limits (Telegram API limits):
  - Photos: 10MB
  - Other files (documents, videos, audio): 50MB
- ✅ Direct download links via HTTP
- ✅ Automatic file cleanup after 24 hours
- ✅ Screen session management
- ✅ Easy update process
- ✅ Nginx reverse proxy for better performance
- ✅ DuckDNS integration for dynamic DNS

## Prerequisites

- Ubuntu server
- Python 3.8 or higher
- Git
- Screen
- Nginx
- DuckDNS account

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

4. Configure Nginx:
```bash
sudo nano /etc/nginx/sites-available/than05.duckdns.org
```
Add the following configuration:
```nginx
server {
    listen 80;
    server_name than05.duckdns.org;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Increase timeouts for large file uploads
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;

        # Increase max body size to 50MB
        client_max_body_size 50M;
    }
}
```

5. Enable the Nginx site:
```bash
sudo ln -s /etc/nginx/sites-available/than05.duckdns.org /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

6. Configure firewall (iptables):
```bash
# Backup current rules
sudo iptables-save > ~/iptables.backup

# Flush existing rules
sudo iptables -F

# Set default policies
sudo iptables -P INPUT ACCEPT
sudo iptables -P FORWARD ACCEPT
sudo iptables -P OUTPUT ACCEPT

# Add essential rules
sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 8080 -j ACCEPT

# Save rules
sudo netfilter-persistent save
```

7. Start the services:
```bash
./start.sh
```

## Usage

### Bot Commands
- `/start` - Start the bot and see welcome message
- `/help` - Show help message with file size limits

### File Sharing
1. Send any supported file to the bot
2. The bot will provide a direct download link
3. Files are automatically cleaned up after 24 hours

### File Size Limits
- Photos: Maximum 10MB
- Documents: Maximum 50MB
- Videos: Maximum 50MB
- Audio files: Maximum 50MB
- Archives (RAR, ZIP): Maximum 50MB

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

### Images (max 10MB)
- JPEG
- PNG
- GIF
- WebP

### Videos (max 50MB)
- MP4
- MOV
- AVI

### Audio (max 50MB)
- MP3
- OGG
- WAV

### Documents (max 50MB)
- PDF
- DOC
- DOCX

### Archives (max 50MB)
- RAR
- ZIP

### Text (max 50MB)
- TXT
- CSV

## Security Features

- ✅ File type validation
- ✅ File size limits
- ✅ Automatic file cleanup
- ✅ CORS support
- ✅ Security headers
- ✅ Nginx reverse proxy
- ✅ Proper firewall configuration

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

### Nginx Issues
Check Nginx status:
```bash
sudo systemctl status nginx
```

Check Nginx logs:
```bash
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Firewall Issues
Check iptables rules:
```bash
sudo iptables -L -n
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.