from telegram import  Update
from telegram.ext import Application, CallbackContext, CommandHandler, ConversationHandler, MessageHandler, filters
from todo_db import init_db, add_todo, get_todos
from dotenv import load_dotenv
import os




load_dotenv()

TOKEN = os.getenv("TOKEN")


async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("enter add todo /todo_add")

todo , time = range(2)

async def todo_start(update: Update, context: CallbackContext):
    await update.message.reply_text("enter todo")
    return todo

async def todo_add(update: Update, context: CallbackContext):
    context.user_data["todo"] = update.message.text
    await update.message.reply_text("enter time")
    return time

async def time_todo_add(update: Update, context: CallbackContext):
    context.user_data["time"] = update.message.text
    add_todo(context.user_data["todo"], context.user_data["time"])
    await update.message.reply_text("your todo created")
    return ConversationHandler.END


async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("cancelling")
    return ConversationHandler.END


async def get_todos_bot(update: Update, context: CallbackContext):
    todos = ""
    for todo in get_todos():
        todos += f"{todo[1]} --> {todo[2]}\n"
    await update.message.reply_text(todos)





def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    conv = ConversationHandler(
        entry_points=[CommandHandler("todo_add", todo_start)],
        states={
            todo :[
                MessageHandler(filters.TEXT & ~filters.COMMAND, todo_add),
            ],
            time :[
                MessageHandler(filters.TEXT & ~filters.COMMAND, time_todo_add),
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
        ]
    )

    app.add_handler(conv)
    app.add_handler(CommandHandler("get_todos", get_todos_bot))

    print("start bot")
    app.run_polling()



if __name__ == "__main__":
    main()