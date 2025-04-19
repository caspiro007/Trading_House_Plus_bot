import os
import json
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Bot token from environment variable or direct string (replace this securely in production)
TOKEN = os.getenv("BOT_TOKEN") or "YOUR_BOT_TOKEN_HERE"
MENU_CONFIG_PATH = 'menu_config.json'

# Admin username
ADMIN_USERNAME = "@Trading_House_Plus_admin"

def is_admin(user):
    return user.username == ADMIN_USERNAME

def load_menu_config():
    if os.path.exists(MENU_CONFIG_PATH):
        with open(MENU_CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return {
            "main_menu": [
                {"label": "مناهج الإنجليزي", "sub_menu": ["سمارت إنجلش", "إنجلش فور أوول", "سمارت كيدز", "سبيك إنجلش", "بيسك إنجلش"]},
                {"label": "مناهج الحاسوب", "sub_menu": ["الحاسوب للجميع ويندوز 7", "الحاسوب للجميع ويندوز 10"]},
                {"label": "مناهج التمهيدي", "sub_menu": ["العب وتعلم نظام المواد كي جي 1", "العب وتعلم نظام المواد كي جي 2", "العب وتعلم نظام الوحدات", "الطفل الذكي"]},
                {"label": "المناهج الملحقة", "sub_menu": ["الخط العربي", "الخط الإنجليزي", "أخلاق وسلوكيات", "التربية الفنية", "نهج تعليم القراءة"]},
                {"label": "للتواصل معنا", "sub_menu": ["عبر الواتساب", "عبر الاتصال", "عبر الفيس بوك"]}
            ],
            "sub_buttons": {
                "سمارت إنجلش": ["الصوتيات", "فلاش كارد", "الفيديوهات", "الاختبارات", "الخطط الدراسية"],
                "إنجلش فور أوول": ["الصوتيات", "فلاش كارد", "الفيديوهات", "الاختبارات", "الخطط الدراسية"],
                "سمارت كيدز": ["الصوتيات", "فلاش كارد", "الفيديوهات", "الاختبارات", "الخطط الدراسية"],
                "سبيك إنجلش": ["الصوتيات", "فلاش كارد", "الفيديوهات", "الاختبارات", "الخطط الدراسية"],
                "بيسك إنجلش": ["الصوتيات", "فلاش كارد", "الفيديوهات", "الاختبارات", "الخطط الدراسية"]
            }
        }

def save_menu_config(config):
    with open(MENU_CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    config = load_menu_config()

    main_menu_buttons = [[KeyboardButton(item["label"])] for item in config["main_menu"]]

    if is_admin(user):
        main_menu_buttons.append([KeyboardButton("لوحة الإدارة")])

    reply_markup = ReplyKeyboardMarkup(main_menu_buttons, resize_keyboard=True)
    await update.message.reply_text("مرحباً بك! اختر من القائمة:", reply_markup=reply_markup)

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("تعديل القائمة الرئيسية")],
        [KeyboardButton("تعديل القوائم الفرعية")],
        [KeyboardButton("⬅️ رجوع")]
    ]
    await update.message.reply_text("لوحة الإدارة:", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user

    if text == "لوحة الإدارة" and is_admin(user):
        await admin(update, context)
        return

    config = load_menu_config()

    # Check if it's a main menu button
    for item in config["main_menu"]:
        if text == item["label"]:
            buttons = [[KeyboardButton(sub)] for sub in item["sub_menu"]]
            await update.message.reply_text("اختر من القائمة:", reply_markup=ReplyKeyboardMarkup(buttons + [[KeyboardButton("⬅️ رجوع")]], resize_keyboard=True))
            return

    # Check if it's a submenu with sub-sub-buttons
    if text in config.get("sub_buttons", {}):
        sub_buttons = config["sub_buttons"][text]
        buttons = [[KeyboardButton(sub)] for sub in sub_buttons]
        await update.message.reply_text("اختر من العناصر:", reply_markup=ReplyKeyboardMarkup(buttons + [[KeyboardButton("⬅️ رجوع")]], resize_keyboard=True))
        return

    if text == "⬅️ رجوع":
        await start(update, context)
        return

    await update.message.reply_text(f"تم استلام: {text}")

# App setup
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...")
app.run_polling()
