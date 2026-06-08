"""
ربات دریافت موقعیت و شماره تماس با استفاده از دکمه‌های ویژه
کاربر می‌تواند با یک کلیک موقعیت یا شماره خود را ارسال کند.
"""

import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = ""

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """نمایش دکمه‌های درخواست موقعیت و شماره"""
    keyboard = [
        [KeyboardButton("📍 ارسال موقعیت", request_location=True)],
        [KeyboardButton("📞 ارسال شماره تماس", request_contact=True)],
        [KeyboardButton("❌ بستن صفحه‌کلید")]
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )
    await update.message.reply_text(
        "لطفاً یکی از گزینه‌های زیر را انتخاب کنید:\n"
        "- ارسال موقعیت مکانی\n"
        "- ارسال شماره تماس\n"
        "- بستن صفحه‌کلید",
        reply_markup=reply_markup
    )

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """دریافت موقعیت مکانی کاربر"""
    location = update.message.location
    await update.message.reply_text(
        f"📍 موقعیت شما دریافت شد:\n"
        f"عرض جغرافیایی: {location.latitude}\n"
        f"طول جغرافیایی: {location.longitude}\n"
        "متشکرم!",
        reply_markup=ReplyKeyboardRemove()   # حذف صفحه‌کلید پس از دریافت
    )

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """دریافت شماره تماس کاربر"""
    contact = update.message.contact
    await update.message.reply_text(
        f"📞 شماره تماس دریافت شد:\n"
        f"نام: {contact.first_name}\n"
        f"شماره: {contact.phone_number}\n"
        "از اعتماد شما سپاسگزاریم.",
        reply_markup=ReplyKeyboardRemove()
    )

async def close_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """بستن صفحه‌کلید بدون دریافت اطلاعات"""
    await update.message.reply_text(
        "صفحه‌کلید بسته شد. برای باز کردن مجدد، /start را وارد کنید.",
        reply_markup=ReplyKeyboardRemove()
    )


async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "لطفا از دستورات بات استفاده کنید /start"
    )

def main() -> None:
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.LOCATION, handle_location))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    app.add_handler(MessageHandler(filters.Regex("^❌ بستن صفحه‌کلید$"), close_keyboard))
    app.add_handler(MessageHandler(~filters.COMMAND & ~filters.Regex("^❌ بستن صفحه‌کلید$"), test))
    logger.info("ربات فعال شد...")
    app.run_polling()

if __name__ == "__main__":
    main()