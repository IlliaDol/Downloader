import os
import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ["TOKEN"]  # токен беремо з Environment Variables у Render

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Надішли мені посилання на відео 🎥")

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    await update.message.reply_text("⏳ Завантажую...")

    # качаємо відео у out.mp4
    cmd = ["yt-dlp", "-f", "bv*+ba/b", "-o", "out.%(ext)s", url]
    subprocess.run(cmd, check=True)

    # відправляємо назад
    with open("out.mp4", "rb") as f:
        await update.message.reply_video(f)

    os.remove("out.mp4")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))
    app.run_polling()

if __name__ == "__main__":
    main()
