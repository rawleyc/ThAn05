# bot.py
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = os.getenv("BASE_URL")

UPLOAD_DIR = "downloads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a file and I'll return a download link.")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Just send any file. I’ll upload and return a link.")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document or update.message.photo[-1] or update.message.video or update.message.audio
    if not file:
        await update.message.reply_text("Unsupported file type.")
        return

    file_name = f"{file.file_unique_id}_{file.file_name or 'file'}"
    file_path = os.path.join(UPLOAD_DIR, file_name)

    telegram_file = await file.get_file()
    await telegram_file.download_to_drive(file_path)

    download_url = f"{BASE_URL}/file/{file_name}"
    await update.message.reply_text(f"Download link: {download_url}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.ALL, handle_file))
    app.run_polling()

if __name__ == "__main__":
    main()
