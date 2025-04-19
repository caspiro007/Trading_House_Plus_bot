import os
import json
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
MENU_CONFIG_PATH = 'menu_config.json'

# Replace with your actual Telegram User ID
ADMIN_USER_ID = "Trading_House_Plus_bot"  # Example: Your user ID

# Load or initialize menu configuration
def load_menu_config():
    if os.path.exists(MENU_CONFIG_PATH):
        with open(MENU_CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return {
            "main_menu": [
                {"label": "مناهج الإنجليزي", "sub_menu": ["سمارت إنجلش", "إنجلش فور أوول", "سمارت كيدز", "سبيك إنجلش", "بيسك إنجلش"]},
                {"label": "مناهج الحاسوب", "sub_menu": ["الحاسوب للجميع ويندوز 7", "الحاسوب للجميع ويندوز 10"]},
                {"label": "مناهج التمهيدي", "sub_menu": ["العب وتعلم نظام المواد كي جي 1", "العب وتعلم نظام المواد كي جي 2"]},
                {"label": "المناهج الملحقة", "sub_menu": ["الخط العربي", "الخط الإنجليزي"]},
                {"label": "للتواصل معنا", "sub_menu": ["عبر الواتساب", "عبر الاتصال", "عبر الفيس بوك"]}
            ],
            "sub_buttons": {
                "سمارت إنجلش": ["الصوتيات", "فلاش كارد", "الفيديوهات", "الاختبارات", "الخطط الدراسية"],
                "إنجلش فور أوول": ["الصوتيات", "فلاش كارد", "الفيديوهات", "الاختبارات", "الخطط الدراسية"],
                "سمارت كيدز": ["الصوتيات", "فلاش كارد", "الفيديوهات", "الاختبارات", "الخطط الدراسية"],
                "سبيك إنجلش": ["الصوتيات", "فلاش كارد", "الفيديوهات", "الاختبارات", "الخطط الدراسية"],
                "بيسك إنجلش": ["الصوتيات", "فلاش كارد", "الفيديوهات", "الاختبارات", "الخطط الدراسية"],
                "الحاسوب للجميع ويندوز 7": ["الملفات", "البرامج", "الدروس"],
                "الحاسوب للجميع ويندوز 10": ["الملفات", "البرامج", "الدروس"]
            }
        }

# Save menu configuration
def save_menu_config(config):
    with open(MENU_CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

# Check if user is admin
def is_admin(user_id):
    return user_id == ADMIN_USER_ID

# Admin commands
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_admin(update.message.from_user.id):
        keyboard = [
            [KeyboardButton("تعديل القائمة الرئيسية")],
            [KeyboardButton("تعديل قائمة فرعية")],
            [KeyboardButton("إلغاء")]
        ]
        await update.message.reply_text("مرحبًا! اختر ما تريد تعديله:", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    else:
        await update.message.reply_text("أنت لست مسؤولًا! لا يمكنك الوصول إلى هذه القائمة.")

async def edit_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_admin(update.message.from_user.id):
        keyboard = [
            [KeyboardButton("إضافة زر رئيسي")],
            [KeyboardButton("حذف زر رئيسي")],
            [KeyboardButton("⬅️ رجوع")]
        ]
        await update.message.reply_text("اختر ما تريد فعله في القائمة الرئيسية:", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    else:
        await update.message.reply_text("أنت لست مسؤولًا! لا يمكنك الوصول إلى هذه القائمة.")

async def edit_sub_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_admin(update.message.from_user.id):
        keyboard = [
            [KeyboardButton("اختيار زر رئيسي لتعديله")],
            [KeyboardButton("⬅️ رجوع")]
        ]
        await update.message.reply_text("اختر الزر الرئيسي الذي تريد تعديل قوائمه الفرعية:", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    else:
        await update.message.reply_text("أنت لست مسؤولًا! لا يمكنك الوصول إلى هذه القائمة.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    config = load_menu_config()

    if text == "/admin":
        await admin(update, context)

    elif text == "تعديل القائمة الرئيسية":
        await edit_main_menu(update, context)

    elif text == "تعديل قائمة فرعية":
        await edit_sub_menu(update, context)

    elif text == "إلغاء":
        await update.message.reply_text("تم إلغاء التعديل.")

    # More handling for adding/removing buttons or updating submenu (to be added)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("admin", admin))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
