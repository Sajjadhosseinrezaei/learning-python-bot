import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler


TOKEN = ""

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


logger = logging.getLogger(__name__)



async def menu(update: Update, context: ContextTypes.DEFAULT_TYPES):

    keyboard = [
        [InlineKeyboardButton("learn", callback_data="learning")],
        [InlineKeyboardButton("opt1", callback_data='option 1'),
         InlineKeyboardButton("opt2", callback_data='option 2')],
        [InlineKeyboardButton('help', callback_data="helping")]
    ]


    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("chose a button", reply_markup=reply_markup)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPES):

    query = update.callback_query
    await query.answer()

    if query.data == "option 1":
        await query.edit_message_text(query.data)

def main():
    app = Application.builder().token(TOKEN).build()
    

    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CallbackQueryHandler(button_handler))
    logger.info("ربات راه‌اندازی شد...")
    app.run_polling()

if __name__ == "__main__":
    main()    
