import os
import json
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    ConversationHandler,
    filters,
)

# Environment Variables
TOKEN = os.getenv("TOKEN")
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID"))

# Paths for persistent storage
BASE_PATH = "/data/party_bot/"
GUEST_FILE = os.path.join(BASE_PATH, "guests.json")
LOG_FILE = os.path.join(BASE_PATH, "bot.log")

# Initialize logging
os.makedirs(BASE_PATH, exist_ok=True)
logging.basicConfig(filename=LOG_FILE, format="%(asctime)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Load or initialize guest data
def load_guests():
    if not os.path.exists(GUEST_FILE):
        return {}
    with open(GUEST_FILE, "r") as file:
        return json.load(file)

def save_guests(guests):
    with open(GUEST_FILE, "w") as file:
        json.dump(guests, file, ensure_ascii=False, indent=4)

guests = load_guests()

# Conversation states
CHOOSING, GET_NAME, GET_SONG, GET_DRESS = range(4)

# Command /start
async def start(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    if user_id in guests and guests[user_id].get("status") == "attending":
        await update.message.reply_text("میدونم میای، دیگه بس کن! 😂")
        return CHOOSING

    reply_keyboard = [["میام", "نمیام", "لیست مهمونا"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("سلام! خوش اومدی 🎉. میای؟ نمیای؟ یا لیست مهمونا؟ 😊", reply_markup=markup)
    return CHOOSING

# Handle user choice
async def handle_choice(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    choice = update.message.text

    if choice == "لیست مهمونا":
        guest_list = "\n".join(
            [
                f"{guest['name']} 🎵 {guest.get('song', 'آهنگ پیشنهاد نشده')} 👕 {guest.get('dress', 'نامشخص')}"
                for guest in guests.values() if guest["status"] == "attending"
            ]
        )
        response = f"لیست مهمونا:\n{guest_list}" if guest_list else "هیچکس هنوز نیومده 😢"
        await update.message.reply_text(response)
        return CHOOSING

    if choice == "نمیام":
        # Remove user from the guest list
        if user_id in guests:
            del guests[user_id]
            save_guests(guests)
        await update.message.reply_text("ایشالا سال دیگه! 😢\nاگه نظرت عوض شد، باز بهم خبر بده.")
        return CHOOSING

    if choice == "میام":
        # Check if the user is already attending
        if user_id in guests and guests[user_id].get("status") == "attending":
            await update.message.reply_text("میدونم میای، دیگه بس کن! 😂")
            return CHOOSING

        # Add user back to the guest list
        guests[user_id] = {"name": None, "song": None, "dress": None, "status": "attending"}
        save_guests(guests)
        await update.message.reply_text("عالیه! اسمت چیه؟", reply_markup=ReplyKeyboardRemove())
        return GET_NAME


# Get name
async def get_name(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    guests[user_id]["name"] = update.message.text
    save_guests(guests)
    await update.message.reply_text("حالا یه آهنگ توپ پیشنهاد بده 🎵")
    return GET_SONG

# Get song
async def get_song(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    guests[user_id]["song"] = update.message.text
    save_guests(guests)
    reply_keyboard = [["کژوال", "رسمی"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("خب، چجوری میای؟ کژوال یا رسمی؟ 👗👔", reply_markup=markup)
    return GET_DRESS

# After choosing the dress code, redirect to the main menu
async def get_dress(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    dress = update.message.text
    if dress not in ["کژوال", "رسمی"]:
        await update.message.reply_text("فقط کژوال یا رسمی انتخاب کن! دوباره بگو.")
        return GET_DRESS

    guests[user_id]["dress"] = dress
    save_guests(guests)

    # Notify completion and return to the main menu
    await update.message.reply_text("خیلی هم عالی، میبینمت! 😍")
    reply_keyboard = [["میام", "نمیام", "لیست مهمونا"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("میخوای دوباره تصمیم بگیری؟ 😎", reply_markup=markup)
    return CHOOSING

# Fallback handler
async def fallback(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("پیام نامعتبره. لطفاً یکی از گزینه‌های منو رو انتخاب کن.")
    return CHOOSING

# Admin command to see stats
async def stats(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id != ADMIN_USER_ID:
        await update.message.reply_text("این دستور فقط برای ادمین هست.")
        return

    total_guests = len([guest for guest in guests.values() if guest["status"] == "attending"])
    response = f"آمار مهمونا:\nکل مهمونا: {total_guests}"
    await update.message.reply_text(response)

# Set up the application
def main():
    application = Application.builder().token(TOKEN).build()

    # Conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_choice)],
            GET_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            GET_SONG: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_song)],
            GET_DRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_dress)],
        },
        fallbacks=[MessageHandler(filters.TEXT | filters.COMMAND, fallback)],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("stats", stats))
    application.run_polling()

if __name__ == "__main__":
    main()
