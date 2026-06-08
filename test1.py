import logging
from dotenv
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes
from datetime import  datetime
from dotenv import  load_dotenv
import os



load_dotenv()
TOKEN = os.getenv("TOKEN")

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# تعریف وضعیت‌ها (مراحل)
NAME, AGE, CONFIRM = range(3)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    # ثبت اطلاعات کاربر در لاگ
    logger.info(
        f"کاربر جدید: ID={user.id}, "
        f"First Name={user.first_name}, "
        f"Last Name={user.last_name}, "
        f"Username=@{user.username if user.username else 'ندارد'}, "
        f"Chat Type={chat.type}, "
        f"Time={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    await update.message.reply_text("سلام! برای ثبت‌نام، دستور /register را بزنید.")
    return ConversationHandler.END  # شروع نکرده، فقط راهنمایی


async def register_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نقطه ورود: شروع مکالمه"""
    await update.message.reply_text("لطفاً نام خود را وارد کنید:")
    return NAME  # برو به مرحله NAME


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دریافت نام و رفتن به مرحله سن"""
    context.user_data['name'] = update.message.text
    await update.message.reply_text(f"خوش آمدید {update.message.text}. حالا سن خود را وارد کنید (فقط عدد):")
    return AGE


async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دریافت سن و رفتن به مرحله تأیید"""
    if not update.message.text.isdigit():
        await update.message.reply_text("لطفاً سن را به صورت عدد وارد کنید:")
        return AGE  # دوباره همین مرحله
    context.user_data['age'] = int(update.message.text)

    # نمایش دکمه‌های تأیید
    keyboard = [["بله", "خیر"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(
        f"نام: {context.user_data['name']}\nسن: {context.user_data['age']}\nآیا اطلاعات صحیح است؟",
        reply_markup=reply_markup
    )
    return CONFIRM


async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تأیید نهایی و پایان مکالمه"""
    if update.message.text == "بله":
        await update.message.reply_text(
            f"✅ ثبت‌نام شما با موفقیت انجام شد.\nنام: {context.user_data['name']}\nسن: {context.user_data['age']}",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await update.message.reply_text("❌ ثبت‌نام لغو شد. برای شروع مجدد /register را بزنید.",
                                        reply_markup=ReplyKeyboardRemove())

    # پاک کردن داده‌های موقت (اختیاری)
    context.user_data.clear()
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """لغو در هر مرحله"""
    await update.message.reply_text("عملیات لغو شد. برای شروع مجدد /register را بزنید.",
                                    reply_markup=ReplyKeyboardRemove())
    context.user_data.clear()
    return ConversationHandler.END


def main():
    app = Application.builder().token(TOKEN).build()

    # ساخت ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("register", register_start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
            CONFIRM: [MessageHandler(filters.Regex("^(بله|خیر)$"), confirm)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)

    logger.info("ربات راه‌اندازی شد...")
    app.run_polling()


if __name__ == "__main__":
    main()