import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes,MessageHandler, filters, CallbackQueryHandler

TOKEN = ""

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__).setLevel(logging.WARNING)
# send a photo from local 
async def send_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    with open("photo.png", "rb") as photo:
        await context.bot.send_photo(chat_id=chat_id, photo=photo, caption="عکس")

# start command for test logger
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"کاربر {user.first_name} (id: {user.id}) دستور /start را اجرا کرد")
    await update.message.reply_text("سلام خوش آمدید!")



async def bug(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        n = int(context.args[0])
        m = 100 / n
        await update.message.reply_text(f"answer {m}")
    except ZeroDivisionError as e:
        logging.exception(f"خطا تقسیم بر صفر")
        await update.message.reply_text("تقسیم بر صفر")
    except (IndexError, ValueError) as e:
        logging.error("ورودی نامعتبر مثل نمونه وارد کن")
        await update.message.reply_text("ورودی نامعتبر مثل نمونه وارد کن /but 5")


# test logger execption and logger error
async def divide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        num = int(context.args[0])
        result = 100 / num
        await update.message.reply_text(f'نتیجه{result}')
    except ZeroDivisionError as e:
        logger.exception("خطا: تقسیم بر صفر")
        await update.message.reply_text("نمیتوان تقسیم بر صفر انجام داد")
    except (IndexError, ValueError) as e:
        logger.error(f"ورودی نامعتبر : {e}")
        await update.message.reply_text("لطفا یک عدد وازد کنید : /divide 5")



# send document from local 
async def send_document(update: Update, context: ContextTypes.DEFAULT_TYPES):

    with open("report.pdf", "rb") as doc:
        await update.message.reply_document(
            document=doc, 
            filename="report.pdf",
            caption="pdf"
        )



def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('send_photo', send_photo))
    app.add_handler(CommandHandler('send_document', send_document))
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('divide', divide))
    app.add_handler(CommandHandler('bug', bug))
    app.run_polling()





if __name__ == '__main__':
    main()