"""
ربات ساده با صفحه‌کلید جایگزین (ReplyKeyboardMarkup)
کاربر با کلیک روی دکمه‌ها می‌تواند غذای مورد نظر را انتخاب کند.
"""

import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# توکن ربات خود را وارد کنید
TOKEN="8688349813:AAHqjsk1zLYf4M_9-YLpluOvJicHqG4qzvo"

# تنظیم لاگ
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ارسال پیام خوش‌آمدگویی و توضیح دستورات"""
    await update.message.reply_text(
        "سلام! به ربات سفارش غذا خوش آمدید.\n"
        "دستور /menu را بزنید تا منو را ببینید."
    )

async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """نمایش صفحه‌کلید جایگزین با گزینه‌های غذا"""
    keyboard = [
        ["🍕 پیتزا", "🍔 برگر"],
        ["🍟 سیب‌زمینی", "🥤 نوشابه"],
        ["❌ لغو سفارش"]
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,       # دکمه‌ها را کوچک و مرتب می‌کند
        one_time_keyboard=False     # صفحه‌کلید پس از یک بار استفاده ناپدید نمی‌شود
    )
    await update.message.reply_text(
        "منوی امروز:\n\n"
        "لطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=reply_markup
    )

async def handle_food_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """پردازش انتخاب کاربر (غذا یا لغو)"""
    user_choice = update.message.text
    valid_foods = ["🍕 پیتزا", "🍔 برگر", "🍟 سیب‌زمینی", "🥤 نوشابه"]

    if user_choice == "❌ لغو سفارش":
        await update.message.reply_text(
            "❌ سفارش شما لغو شد.\n"
            "برای دیدن منوی جدید، /menu را وارد کنید.",
            reply_markup=ReplyKeyboardRemove()   # حذف صفحه‌کلید
        )
    elif user_choice in valid_foods:
        context.user_data['order'] = user_choice
        await update.message.reply_text(
            f"✅ سفارش شما ثبت شد: {user_choice}\n"
            "از خرید شما متشکریم!\n"
            "برای سفارش مجدد /menu را بزنید.",
            reply_markup=ReplyKeyboardRemove()   # حذف صفحه‌کلید پس از ثبت سفارش
        )
    else:
        # اگر کاربر چیزی خارج از دکمه‌ها تایپ کرد
        await update.message.reply_text(
            "❌ گزینه نامعتبر است. لطفاً از دکمه‌های منو استفاده کنید.\n"
            "برای مشاهده منو، /menu را وارد کنید."
        )

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """دستور /cancel برای حذف صفحه‌کلید در هر شرایطی"""
    await update.message.reply_text(
        "عملیات لغو شد. صفحه‌کلید حذف گردید.",
        reply_markup=ReplyKeyboardRemove()
    )

def main() -> None:
    """راه‌اندازی ربات"""
    app = Application.builder().token(TOKEN).build()

    # هندلرهای دستورات
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", show_menu))
    app.add_handler(CommandHandler("cancel", cancel))

    # هندلر پیام‌های متنی (به جز دستورات)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_food_choice))

    logger.info("ربات شروع به کار کرد...")
    app.run_polling(allowed_updates=[])

if __name__ == "__main__":
    main()