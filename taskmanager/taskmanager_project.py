import os
from init_database import init_db, create_task, retrieve_tasks, update_task, delete_task, get_all_tasks
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


async def get_all_tasks_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["chat_id"] = update.message.chat.id
    context.user_data["user_id"] = update.message.from_user.id

    tasks = get_all_tasks(context.user_data["user_id"], context.user_data["chat_id"])

    if not tasks:
        await update.message.reply_text("📋 شما هیچ تسکی ندارید.")
        return

    text_reply = "📋 **تسک‌های شما:**\n\n"

    for task in tasks:
        try:
            id, title, status = task
            text_reply += f"🔹{id} - {title} - {status}\n"
        except ValueError:
            text_reply += f"🔹 {task[0]} - (بدون وضعیت)\n"

    await update.message.reply_text(text_reply, parse_mode="Markdown")


DEL = 1

async def get_id_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ID تسک را وارد کنید")
    return DEL

async def delete_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    id = update.message.text
    user_id = update.message.from_user.id
    if not id.isdigit():
        await update.message.reply_text("آیدی باید عدد باشد")
        return DEL

    status = delete_task(int(id), int(user_id))
    if status:
        await update.message.reply_text(
            f"🗑️ تسک با شناسه {id} با موفقیت حذف شد."
        )
    else:
        await update.message.reply_text("نمیتوان این تسک را حذف کرد")

    return ConversationHandler.END

ID, U_TITLE, STATUS = range(3)
async def update_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("آیدی تسک را وارد کنید")
    return ID

async def get_id_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    id = update.message.text
    if not id.isdigit():
        await update.message.reply_text("آیدی باید عدد باشد")
        return ID

    context.user_data['id'] = int(id)
    await update.message.reply_text("حالا عنوان جدید را وارد کنید")
    return U_TITLE

async def get_u_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['title'] = update.message.text
    keyboard = [["Low", "Medium", "High"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("وضعیت را وارد کنید", reply_markup=reply_markup)
    return STATUS

async def get_u_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    id = context.user_data['id']
    user_id = update.message.from_user.id
    title = context.user_data['title']
    status = update.message.text
    updated = update_task(id, user_id, title, status)
    if updated:
        await update.message.reply_text(
            "✅ تسک با موفقیت ویرایش شد.", reply_markup=ReplyKeyboardRemove()
        )
    else:
        await update.message.reply_text(
            "❌ ویرایش انجام نشد! (تسک یافت نشد یا دسترسی ندارید)",
            reply_markup=ReplyKeyboardRemove(),
        )

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

    task_delete_handler = ConversationHandler(
        entry_points=[CommandHandler("delete", get_id_delete)],
        states={
            DEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, delete_tasks)]
        },
        fallbacks=[CommandHandler("cancel", cancel_task)],
    )
    task_update_handler = ConversationHandler(
        entry_points=[CommandHandler("edit", update_tasks)],
        states={
            ID : [MessageHandler(filters.TEXT & ~filters.COMMAND, get_id_update)],
            U_TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_u_title)],
            STATUS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_u_status)],
        },
        fallbacks=[CommandHandler("cancel", cancel_task)],
    )
    app.add_handler(task_conv_handler)
    app.add_handler(task_delete_handler)
    app.add_handler(task_update_handler)
    app.add_handler(CommandHandler("tasks", get_all_tasks_user))
    print("bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()