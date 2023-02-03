import logging
import telegram
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, filters, ConversationHandler, ApplicationBuilder)
import os
import mysql.connector

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

STUDENT_NUMBER, FNAME, LNAME, SEX, CONFIRMATION = range(5)

TOKEN = "5806507050:AAFVm2zmYpAxDwjQtXr_MaROnYM_eZG8gwI"
bot = telegram.Bot(token=TOKEN)

PORT = int(os.environ.get('PORT', 5000))

reply_keyboard = [['شروع دوباره', 'مورد تایید است']]
reply_keyboard_sex = [['زن', 'مرد']]
markup_sex = ReplyKeyboardMarkup(reply_keyboard_sex, resize_keyboard=True, one_time_keyboard=True)
markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)


async def start(update, context):
    await update.message.reply_text(
        "سلام من ربات مدیریت کلاس برنامه سازی پیشرفته هستم.اگه میخوای توی این کلاس شرکت کنی شماره دانشجوییت رو برام "
        "بنویس")
    return STUDENT_NUMBER


async def student_number(update, context):
    user = update.message.from_user
    user_data = context.user_data
    category = 'شماره دانشجویی'
    text = update.message.text
    user_data[category] = text

    logger.info("student number of %s: %s", user.first_name, update.message.text)

    await update.message.reply_text("خب؛ شماره دانشجوییت ثبت شد.")
    await update.message.reply_text("حالا اسمت رو برام بنویس.")

    return FNAME


async def fname(update, context):
    user = update.message.from_user
    user_data = context.user_data
    category = 'نام'
    text = update.message.text
    user_data[category] = text

    logger.info("first name of %s: %s", user.first_name, update.message.text)

    await update.message.reply_text("حالا نام خانوادگیت رو بنویس.")

    return LNAME


async def lname(update, context):
    user = update.message.from_user
    user_data = context.user_data
    category = 'نام خانوادگی'
    text = update.message.text
    user_data[category] = text

    logger.info("last name of %s: %s", user.first_name, update.message.text)

    await update.message.reply_text("بسیار عالی؛ حالا جنسیت خودت رو انتخاب کن.", reply_markup=markup_sex)

    return SEX


def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])


async def sex(update, context):
    user = update.message.from_user
    user_data = context.user_data
    category = 'جنسیت'

    text = update.message.text
    user_data[category] = text

    logger.info("sex of %s: %s", user.first_name, update.message.text)

    await update.message.reply_text(
        'از این که اطلاعات را برای ما ارسال کردین سپاس گزاریم . لطفا بررسی کنید که آیا اطلاعات مورد تاییدتان است یا '
        'نه {}'.format(
            facts_to_str(user_data)),
        reply_markup=markup)

    return CONFIRMATION


async def confirmation(update, context):
    user = update.message.from_user
    user_data = context.user_data
    logger.info("User %s added to the class", user.first_name)
    await update.message.reply_text("نام شما در کلاس ثبت شد!")

    return ConversationHandler.END


async def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the coneversation", user.first_name)

    await update.message.reply_text("بدرود امیدوارم بازم شما رو ببینم", reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    app = ApplicationBuilder().token("5806507050:AAFVm2zmYpAxDwjQtXr_MaROnYM_eZG8gwI").build()


    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            STUDENT_NUMBER: [CommandHandler('start', start), MessageHandler(filters.TEXT, student_number)],
            FNAME: [CommandHandler('start', start), MessageHandler(filters.TEXT, fname)],
            LNAME: [CommandHandler('start', start), MessageHandler(filters.TEXT, lname)],
            SEX: [CommandHandler('start', start), MessageHandler(filters.TEXT, sex)],
            CONFIRMATION: [CommandHandler('start', start),
                           MessageHandler(filters.Regex('^مورد تایید است$'), confirmation),
                           MessageHandler(filters.Regex('^شروع دوباره$'), start)]
        },

        fallbacks=[CommandHandler('cancle', cancel)]
    )

    # app.run_webhook(listen='0.0.0.0', port=PORT, url_path=TOKEN)
    # telegram.Bot.set_webhook('https://cb7921f3.ngrok.io/' + TOKEN)

    app.add_handler(conv_handler)
    app.run_polling()


if __name__ == '__main__':

    main()
