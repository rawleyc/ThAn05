# bot.py
import os
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import aiohttp
import aiofiles
import uuid
import mimetypes

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
BASE_URL = os.getenv('BASE_URL')
FILES_DIR = os.getenv('FILES_DIR', 'files')

# Constants
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB (Telegram's limit for regular bots)
MAX_PHOTO_SIZE = 10 * 1024 * 1024  # 10MB (Telegram's limit for photos)
ALLOWED_MIME_TYPES = {
    'image/jpeg', 'image/png', 'image/gif', 'image/webp',
    'video/mp4', 'video/quicktime', 'video/x-msvideo',
    'audio/mpeg', 'audio/ogg', 'audio/wav',
    'application/pdf', 'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'text/plain', 'text/csv',
    'application/x-rar-compressed', 'application/rar',  # RAR files
    'application/zip', 'application/x-zip-compressed'   # ZIP files
}

# Add RAR MIME type to mimetypes
mimetypes.add_type('application/x-rar-compressed', '.rar')
mimetypes.add_type('application/rar', '.rar')

# Ensure files directory exists
os.makedirs(FILES_DIR, exist_ok=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    welcome_message = (
        "👋 Welcome to the File Sharing Bot!\n\n"
        "📤 Send me any file and I'll provide you with a direct download link.\n\n"
        "📋 File size limits:\n"
        f"• Photos: {MAX_PHOTO_SIZE // (1024 * 1024)}MB\n"
        f"• Other files: {MAX_FILE_SIZE // (1024 * 1024)}MB\n\n"
        "📚 Use /help to see all available commands and supported file types."
    )
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    help_message = (
        "📚 Available Commands:\n\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n\n"
        "📤 Supported File Types:\n"
        "• Images (JPEG, PNG, GIF, WebP) - max 10MB\n"
        "• Videos (MP4, MOV, AVI) - max 50MB\n"
        "• Audio (MP3, OGG, WAV) - max 50MB\n"
        "• Documents (PDF, DOC, DOCX) - max 50MB\n"
        "• Archives (RAR, ZIP) - max 50MB\n"
        "• Text (TXT, CSV) - max 50MB\n\n"
        "⚠️ Files are automatically deleted after 24 hours."
    )
    await update.message.reply_text(help_message)

def is_file_allowed(file_name: str, mime_type: str = None) -> bool:
    """Check if the file type is allowed."""
    # Check file extension
    ext = os.path.splitext(file_name)[1].lower()
    if ext in ['.rar', '.zip']:
        return True
        
    # Check MIME type
    if mime_type:
        return mime_type in ALLOWED_MIME_TYPES
        
    # Fallback to mimetypes guess
    guessed_type = mimetypes.guess_type(file_name)[0]
    return guessed_type in ALLOWED_MIME_TYPES

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle document files."""
    if update.message.document.file_size > MAX_FILE_SIZE:
        await update.message.reply_text(f"❌ File is too large. Maximum size is {MAX_FILE_SIZE // (1024 * 1024)}MB")
        return
    
    if not is_file_allowed(update.message.document.file_name, update.message.document.mime_type):
        await update.message.reply_text("❌ This file type is not allowed.")
        return

    file = await update.message.document.get_file()
    file_name = update.message.document.file_name
    await download_and_send_link(update, file, file_name)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle photo files."""
    photo = update.message.photo[-1]  # Get the highest quality photo
    if photo.file_size > MAX_PHOTO_SIZE:
        await update.message.reply_text(f"❌ Photo is too large. Maximum size is {MAX_PHOTO_SIZE // (1024 * 1024)}MB")
        return

    file = await photo.get_file()
    file_name = f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    await download_and_send_link(update, file, file_name)

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle video files."""
    if update.message.video.file_size > MAX_FILE_SIZE:
        await update.message.reply_text(f"❌ Video is too large. Maximum size is {MAX_FILE_SIZE // (1024 * 1024)}MB")
        return

    video = update.message.video
    file = await video.get_file()
    file_name = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    await download_and_send_link(update, file, file_name)

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle audio files."""
    if update.message.audio.file_size > MAX_FILE_SIZE:
        await update.message.reply_text(f"❌ Audio file is too large. Maximum size is {MAX_FILE_SIZE // (1024 * 1024)}MB")
        return

    audio = update.message.audio
    file = await audio.get_file()
    file_name = audio.file_name or f"audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    await download_and_send_link(update, file, file_name)

async def download_and_send_link(update: Update, file, file_name):
    """Download file and send the download link."""
    try:
        # Generate unique filename
        unique_id = str(uuid.uuid4())[:8]
        file_extension = os.path.splitext(file_name)[1]
        unique_filename = f"{unique_id}{file_extension}"
        file_path = os.path.join(FILES_DIR, unique_filename)

        # Download file
        await file.download_to_drive(file_path)
        
        # Generate download link
        download_url = f"{BASE_URL}/{unique_filename}"
        
        # Send confirmation message
        await update.message.reply_text(
            f"✅ File uploaded successfully!\n\n"
            f"📥 Download link:\n{download_url}"
        )
    except Exception as e:
        logger.error(f"Error handling file: {e}")
        await update.message.reply_text("❌ Sorry, there was an error processing your file. Please try again.")

def main():
    """Start the bot."""
    if not all([BOT_TOKEN, BASE_URL]):
        logger.error("Missing required environment variables: BOT_TOKEN, BASE_URL")
        return

    if not os.path.exists(FILES_DIR):
        logger.error(f"Files directory {FILES_DIR} does not exist and could not be created")
        return

    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))
    application.add_handler(MessageHandler(filters.AUDIO, handle_audio))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
