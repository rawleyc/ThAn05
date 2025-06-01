# Telegram File Sharing Bot

A Telegram bot that allows users to share files and get direct download links. The bot downloads files to a server and provides HTTP URLs for downloading them.

## Features

- Accepts various file types (documents, photos, videos, audio)
- Generates unique filenames to prevent conflicts
- Provides direct download links
- Simple Flask server for file hosting
- Screen sessions for process management

## Prerequisites

- Ubuntu 20.04 or later
- Python 3.8 or later
- Oracle Cloud VM instance
- Telegram Bot Token (get from @BotFather)

## Installation

1. **Update system and install dependencies**

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install python3-pip python3-venv nginx screen -y
```

2. **Create project directory**

```bash
mkdir -p ~/telegram-file-bot
cd ~/telegram-file-bot
```

3. **Set up Python virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the project directory:

```bash
nano .env
```

Add the following content (replace with your values):

```
BOT_TOKEN=your_telegram_bot_token
BASE_URL=http://your-server-ip:8080
FILES_DIR=/home/ubuntu/telegram-file-bot/files
```

5. **Make scripts executable**

```bash
chmod +x start.sh stop.sh
```

6. **Start the services**

```bash
./start.sh
```

This will start both the bot and the file server in separate screen sessions.

## Managing the Services

### Viewing Logs

To view the bot logs:
```bash
screen -r telegram-bot
```

To view the server logs:
```bash
screen -r file-server
```

To detach from a screen session (leave it running in the background):
- Press `Ctrl+A`, then `D`

### Stopping Services

To stop both services:
```bash
./stop.sh
```

## Optional: Nginx Configuration with SSL

1. **Install Certbot**

```bash
sudo apt install certbot python3-certbot-nginx -y
```

2. **Create Nginx configuration**

```bash
sudo nano /etc/nginx/sites-available/telegram-bot
```

Add the following configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

3. **Enable the site and get SSL certificate**

```bash
sudo ln -s /etc/nginx/sites-available/telegram-bot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
sudo certbot --nginx -d your-domain.com
```

4. **Update BASE_URL in .env**

After setting up SSL, update the BASE_URL in your .env file to use HTTPS:

```
BASE_URL=https://your-domain.com
```

Then restart the services:

```bash
./stop.sh
./start.sh
```

## Usage

1. Start a chat with your bot on Telegram
2. Send any file (document, photo, video, or audio)
3. The bot will respond with a direct download link

## Troubleshooting

- Check if services are running:
  ```bash
  screen -ls
  ```

- Ensure ports are open:
  ```bash
  sudo ufw allow 80/tcp
  sudo ufw allow 443/tcp
  ```

- Check file permissions:
  ```bash
  sudo chown -R ubuntu:ubuntu ~/telegram-file-bot
  ```

## Security Considerations

1. Keep your BOT_TOKEN secure
2. Regularly update system and Python packages
3. Consider implementing rate limiting
4. Monitor server resources and disk space
5. Back up important files regularly

## License

MIT License