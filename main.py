import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# File to store the data (e.g., "files_data.json")
FILES_DATA_PATH = "files_data.json"

# Admin's Telegram ID (You need to replace this with your actual Telegram ID)
ADMIN_ID = 7350426578

# Function to load file storage data from the JSON file
def load_file_storage():
    try:
        with open(FILES_DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Function to save file storage data to the JSON file
def save_file_storage(data):
    with open(FILES_DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Function to check if the user is the admin
def is_admin(update: Update):
    return update.message.from_user.id == ADMIN_ID

# Function to start the admin panel
async def start_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_admin(update):
        await update.message.reply_text(
            "Welcome Admin! You can upload files and assign them to categories.\n"
            "Send a file, and I will ask you where to store it."
        )
    else:
        await update.message.reply_text("You are not authorized to access this admin panel.")

# Function to handle file uploads and ask where to store
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_admin(update):
        # Ask the admin to provide a category and grade for the file
        await update.message.reply_text(
            "Please specify where to store this file (category and grade).\n"
            "Example: 'الصوتيات → الصف الأول'."
        )
        # Store the file temporarily until the admin gives a category
        file_id = update.message.document.file_id
        file_name = update.message.document.file_name
        # Store temporarily in context.user_data
        context.user_data['temp_file'] = {'file_id': file_id, 'file_name': file_name}
    else:
        await update.message.reply_text("You are not authorized to upload files.")

# Function to process the file location (category and grade)
async def process_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_admin(update):
        if 'temp_file' in context.user_data:
            # Extract the file data
            file_data = context.user_data['temp_file']
            file_id = file_data['file_id']
            file_name = file_data['file_name']

            # Get the category and grade from the admin's message
            location = update.message.text.strip()
            
            # Load current file storage
            file_storage = load_file_storage()

            # Save the file under the specified category and grade
            if location not in file_storage:
                file_storage[location] = []
            file_storage[location].append(file_id)

            # Save the updated file storage to the JSON file
            save_file_storage(file_storage)

            # Respond back to admin
            await update.message.reply_text(
                f"File '{file_name}' saved under {location}.\n"
                "Now you can send this file to users when they select the category."
            )

            # Clean up temporary file data
            del context.user_data['temp_file']
        else:
            await update.message.reply_text("No file to store! Please send a file first.")
    else:
        await update.message.reply_text("You are not authorized to modify files.")

# Function to send files to users based on the selected category
async def send_category_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    category = ' '.join(context.args)  # Get category from the command (e.g., الصوتيات)
    
    # Load the file storage
    file_storage = load_file_storage()

    if category in file_storage:
        # Send all files in the selected category
        files = file_storage[category]
        
        # Check if there are multiple files or just one
        if len(files) > 1:
            for file_id in files:
                await update.message.reply_document(document=file_id)
        else:
            # Send single file if there's only one
            await update.message.reply_document(document=files[0])
    else:
        await update.message.reply_text(f"No files available for category: {category}")

# Initialize the bot
app = ApplicationBuilder().token("7687273221:AAGAC5DmtQHSh5C2C0BRT61d7xZHJpa9GJs").build()

# Add handlers
app.add_handler(CommandHandler("start", start_admin))  # Admin start command
app.add_handler(MessageHandler(filters.DOCUMENT, handle_document))  # Handle document uploads
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_location))  # Handle location processing
app.add_handler(CommandHandler("sendfile", send_category_file))  # Send files to users based on category

# Run the bot
app.run_polling()
