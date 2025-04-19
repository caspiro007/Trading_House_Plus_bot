import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# Main menu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("مناهج الإنجليزي", callback_data='menu_docs')],
        [InlineKeyboardButton("مناهج الحاسوب", callback_data='menu_media')],
        [InlineKeyboardButton("مناهج التمهيدي", callback_data='menu_apps')]
        [InlineKeyboardButton("المناهج الملحقة", callback_data='menu_appss')]
        [InlineKeyboardButton(" للتواصل معنا", callback_data='menu_appsss')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Main Menu:", reply_markup=reply_markup)

# Callback query handler for all buttons
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    # Sub-menus
    if data == 'menu_docs':
        keyboard = [
            [InlineKeyboardButton("PDF", callback_data='file_pdf')],
            [InlineKeyboardButton("ZIP", callback_data='file_zip')],
            [InlineKeyboardButton("⬅️ Back", callback_data='back_main')]
        ]
        await query.edit_message_text("Documents:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == 'menu_media':
        keyboard = [
            [InlineKeyboardButton("Image", callback_data='file_image')],
            [InlineKeyboardButton("Video", callback_data='file_video')],
            [InlineKeyboardButton("Audio", callback_data='file_audio')],
            [InlineKeyboardButton("⬅️ Back", callback_data='back_main')]
        ]
        await query.edit_message_text("Media:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == 'menu_apps':
        keyboard = [
            [InlineKeyboardButton("PDF", callback_data='file_pdf')],
            [InlineKeyboardButton("ZIP", callback_data='file_zip')],
            [InlineKeyboardButton("⬅️ Back", callback_data='back_main')]
        ]
        await query.edit_message_text("Apps:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == 'menu_appss':
        keyboard = [
            [InlineKeyboardButton("PDF", callback_data='file_pdf')],
            [InlineKeyboardButton("ZIP", callback_data='file_zip')],
            [InlineKeyboardButton("⬅️ Back", callback_data='back_main')]
        ]
        await query.edit_message_text("Apps:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == 'menu_appsss':
        keyboard = [
            [InlineKeyboardButton("PDF", callback_data='file_pdf')],
            [InlineKeyboardButton("ZIP", callback_data='file_zip')],
            [InlineKeyboardButton("⬅️ Back", callback_data='back_main')]
        ]
        await query.edit_message_text("Apps:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == 'back_main':
        await start(update, context)

    # Sending actual files
    else:
        file_map = {
            'file_pdf': ('files/sample.pdf', 'document'),
            'file_zip': ('files/sample.zip', 'document'),
            'file_image': ('files/sample.jpg', 'photo'),
            'file_video': ('files/sample.mp4', 'video'),
            'file_audio': ('files/sample.mp3', 'audio'),
            'file_apk': ('files/sample.apk', 'document'),
            'file_iso': ('files/sample.iso', 'document')
        }

        file_path, method = file_map.get(data, (None, None))

        if not file_path or not os.path.exists(file_path):
            await query.edit_message_text("File not found.")
            return

        if method == 'document':
            await query.message.reply_document(open(file_path, "rb"))
        elif method == 'video':
            await query.message.reply_video(open(file_path, "rb"))
        elif method == 'photo':
            await query.message.reply_photo(open(file_path, "rb"))
        elif method == 'audio':
            await query.message.reply_audio(open(file_path, "rb"))

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()
