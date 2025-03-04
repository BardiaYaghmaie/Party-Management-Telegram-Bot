import os
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
from guest_manager import GuestManager

# Environment Variables
TOKEN = os.getenv("TOKEN")
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID"))

# Initialize logging with detailed format
LOG_FILE = os.path.join("/data/party_bot/", "bot.log")
os.makedirs("/data/party_bot/", exist_ok=True)
logging.basicConfig(filename=LOG_FILE, format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize GuestManager
guest_manager = GuestManager()

# Conversation states
CHOOSING, GET_NAME, GET_SONG, GET_DRESS = range(4)

# Main menu markup
main_menu = ReplyKeyboardMarkup([["میام", "نمیام", "لیست مهمونا"]], one_time_keyboard=True, resize_keyboard=True)


async def start(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    logger.info(f"User {user_id} initiated /start")
    if user_id in guest_manager.guests and guest_manager.guests[user_id].get("status") == "attending":
        logger.info(f"User {user_id} already attending; showing main menu")
        await update.message.reply_text("میدونم میای، دیگه بس کن! 😂", reply_markup=main_menu)
        return CHOOSING

    await update.message.reply_text("سلام خوبی؟ 🥳\nمیای؟ نمیای؟ یا لیست مهمونا؟", reply_markup=main_menu)
    return CHOOSING


async def handle_choice(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    choice = update.message.text
    logger.info(f"User {user_id} made a choice: {choice}")

    if choice == "لیست مهمونا":
        guest_list = "\n".join(
            [
                f"{guest['name']} 🎵 {guest.get('song', 'آهنگ پیشنهاد نشده')} 👕 {guest.get('dress', 'نامشخص')}"
                for guest in guest_manager.guests.values()
                if guest["status"] == "attending"
            ]
        )
        response = f"لیست مهمونا:\n{guest_list}" if guest_list else "هیچکس هنوز نیومده 😢"
        logger.info(f"User {user_id} requested guest list. Response: {response}")
        await update.message.reply_text(response, reply_markup=main_menu)
        return CHOOSING

    if choice == "نمیام":
        if user_id in guest_manager.guests:
            guest_manager.remove_guest(user_id)
            logger.info(f"User {user_id} removed from guest list (status: نمیام)")
            await guest_manager.save_guests_async()
        await update.message.reply_text(
            "ایشالا سال دیگه! 😢\nاگه نظرت عوض شد، باز بهم خبر بده.", reply_markup=main_menu
        )
        return CHOOSING

    if choice == "میام":
        if user_id in guest_manager.guests and guest_manager.guests[user_id].get("status") == "attending":
            logger.info(f"User {user_id} already marked as attending")
            await update.message.reply_text("میدونم میای، دیگه بس کن! 😂", reply_markup=main_menu)
            return CHOOSING

        guest_manager.add_guest(user_id, {"name": None, "song": None, "dress": None, "status": "attending"})
        logger.info(f"User {user_id} added as attending; awaiting name")
        await guest_manager.save_guests_async()
        await update.message.reply_text("عالیه! اسمت چیه؟", reply_markup=ReplyKeyboardRemove())
        return GET_NAME


async def get_name(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    name = update.message.text
    guest_manager.guests[user_id]["name"] = name
    logger.info(f"User {user_id} provided name: {name}")
    await guest_manager.save_guests_async()
    await update.message.reply_text("حالا یه آهنگ واسه پلی‌لیست پیشنهاد بده 🎵")
    return GET_SONG


async def get_song(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    song = update.message.text

    if not isinstance(song, str) or song.strip() == "":
        logger.warning(f"User {user_id} provided invalid song input")
        await update.message.reply_text("لطفاً فقط اسم آهنگ رو بنویسید و فایل یا چیز دیگه نفرستید. 🎵")
        return GET_SONG

    guest_manager.guests[user_id]["song"] = song.strip()
    logger.info(f"User {user_id} provided song: {song.strip()}")
    await guest_manager.save_guests_async()

    reply_keyboard = [["کژوال", "رسمی"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("خب، چجوری میای؟ کژوال یا رسمی؟ 👗👔", reply_markup=markup)
    return GET_DRESS


async def get_dress(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    dress = update.message.text
    if dress not in ["کژوال", "رسمی"]:
        logger.warning(f"User {user_id} provided invalid dress input: {dress}")
        await update.message.reply_text("فقط کژوال یا رسمی انتخاب کن! دوباره بگو.")
        return GET_DRESS

    guest_manager.guests[user_id]["dress"] = dress
    logger.info(f"User {user_id} selected dress: {dress}")
    await guest_manager.save_guests_async()

    await update.message.reply_text("آقا عالی، میبینمت 🥹", reply_markup=main_menu)
    return CHOOSING


async def fallback(update: Update, context: CallbackContext) -> int:
    logger.warning("Fallback triggered due to invalid input")
    await update.message.reply_text("پیام نامعتبره. لطفاً یکی از گزینه‌های منو رو انتخاب کن.", reply_markup=main_menu)
    return CHOOSING


async def stats(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    logger.info(f"User {user_id} requested stats")
    if user_id != ADMIN_USER_ID:
        logger.warning(f"Unauthorized stats request by user {user_id}")
        await update.message.reply_text("این دستور فقط برای ادمین هست.")
        return

    total_guests = len([guest for guest in guest_manager.guests.values() if guest["status"] == "attending"])
    response = f"آمار مهمونا:\nکل مهمونا: {total_guests}"
    logger.info(f"Stats provided to admin: {response}")
    await update.message.reply_text(response)


def main():
    application = Application.builder().token(TOKEN).build()

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
    logger.info("Bot is starting polling...")
    application.run_polling()


if __name__ == "__main__":
    main()
