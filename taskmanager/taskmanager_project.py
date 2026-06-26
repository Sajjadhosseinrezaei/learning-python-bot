import os
from init_database import init_db, create_task, retrieve_tasks, update_task, delete_task
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, ContextTypes, CommandHandler, ConversationHandler, MessageHandler, filters
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

TITLE ,STATE = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("به Task Manager خوش آمدی."
                                    "\n"
                                    "دستورات:"
                                    "\n"
                                    "/addtask\n"
                                    "/tasks\n"
                                    "/edit\n"
                                    "/delete \n"
                                    "/search \n"
                                    "/stats \n")


async def start_get_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("عنوان تسک را وارد کنید")
    return TITLE

async def get_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['title'] = update.message.text
    keyboard = [["Low", "Medium", "High"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("وضعیت را وارد کنید", reply_markup=reply_markup)
    return STATE


async def get_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chosen_state = update.message.text

    if chosen_state not in ["Low", "Medium", "High"]:
        await update.message.reply_text("فقط از دکمه های زیر استفاده کنید")
        return STATE

    context.user_data['state'] = chosen_state
    title = context.user_data['title']
    state = context.user_data['state']
    user_id = update.message.from_user.id
    chat_id = update.message.chat.id

    create_task(title, state, user_id, chat_id)
    await update.message.reply_text(
            f"تسک '{title}' با وضعیت '{state}' با موفقیت ذخیره شد! ✅",
            reply_markup=ReplyKeyboardRemove(),  # کیبورد قبلی را غیب می‌کند
        )

        # ۸. پاک کردن حافظه موقت برای تسک‌های بعدی و پایان گفتگو
    context.user_data.clear()
    return ConversationHandler.END


async def cancel_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("عملیات کنسل شد")
    context.user_data.clear()
    return ConversationHandler.END








def main():
    init_db()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    task_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("addtask", start_get_task)],
        states={
            TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_task)],
            STATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_stats)],

        },
        fallbacks=[
            CommandHandler("cancel", cancel_task),
        ]

    )

    app.add_handler(task_conv_handler)
    print("bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()