import logging
from multiprocessing.reduction import register

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes, \
    CallbackContext, CallbackQueryHandler, Updater
from datetime import  datetime
from dotenv import  load_dotenv
import os



load_dotenv()
TOKEN = os.getenv("TOKEN")


reply_keyboard = [
    ["mobile", " laptop"],
]

reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)


inline_keyboard_phone = [
    [
        InlineKeyboardButton("iphone", callback_data="iphone"),
        InlineKeyboardButton("samsung", callback_data="samsung"),
    ]
]

inline_keyboard_laptop = [
    [
        InlineKeyboardButton("lenovo", callback_data="lenovo"),
        InlineKeyboardButton("Asus", callback_data="Asus"),
    ]
]

mobile_reply_markup_inline_keyboard = InlineKeyboardMarkup(inline_keyboard_phone)
laptop_reply_markup_inline_keyboard = InlineKeyboardMarkup(inline_keyboard_laptop)




async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("choise your product", reply_markup=reply_markup)



async def message_handler(update: Update, context: CallbackContext):
    text = update.message.text
    if text == "mobile":
        await update.message.reply_text("enter your product", reply_markup=mobile_reply_markup_inline_keyboard)

    if text == "laptop":
        await  update.message.reply_text("enter your product", reply_markup=laptop_reply_markup_inline_keyboard)



async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == "iphone":
        await query.edit_message_text("your choice is iphone")

    if query.data == "samsung":
        await query.edit_message_text("your choice is samsung")

    if query.data == "lenovo":
        await query.edit_message_text("your choice is lenovo")

    if query.data == "Asus":
        await query.edit_message_text("your choice is Asus")



NAME, AGE = range(2)


async def register(update: Update, context: CallbackContext):
    await update.message.reply_text("enter your name")
    return NAME


async def get_name(update: Update, context: CallbackContext):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("enter your age")
    return AGE

async def get_age(update: Update, context: CallbackContext):
    context.user_data["age"] = update.message.text
    await update.message.reply_text(f"you registered\n{context.user_data['name']}\n"
                                    f"{context.user_data['age']}")
    return ConversationHandler.END


async def cancel_handler(update: Update, context: CallbackContext):
    await update.message.reply_text("cancel your operation")
    return ConversationHandler.END

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler("register", register)],
        states={
            NAME:[MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            AGE:[MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
        },
        fallbacks=[CommandHandler("cancel", cancel_handler)]
    ))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("start")
    app.run_polling()



if __name__ == "__main__":
    main()