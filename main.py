import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Use /pdf /video /image etc.")

async def pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_document(open("files/sample.pdf", "rb"))

async def video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_video(open("files/sample.mp4", "rb"))

async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(open("files/sample.jpg", "rb"))

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("pdf", pdf))
app.add_handler(CommandHandler("video", video))
app.add_handler(CommandHandler("image", image))

app.run_polling()
