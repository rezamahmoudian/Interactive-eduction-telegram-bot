from __future__ import print_function
import logging
import telegram
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, filters, ConversationHandler, ApplicationBuilder)
import os
import mysql.connector
from mysql.connector import errorcode


# cnx = mysql.connector.connect(user='root', password='1234',
#                               host='127.0.0.1',
#                               database='telegram-bot')
# cnx.close()

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
    user = update.message.from_user
    user_data = context.user_data
    # print(user[1])
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

    await update.message.reply_text("چ اسم قشنگی☺️")
    await update.message.reply_text("حالا فامیلیت رو هم برام بنویس.")

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


DB_NAME = 'telegram_bot'
TABLES = {}
TABLES['students'] = (
    "CREATE TABLE `student` ("
    "  `id` int(11) NOT NULL,"
    "  `student_number` int(8) NOT NULL,"
    "  `first_name` varchar(14) NOT NULL,"
    "  `last_name` varchar(16) NOT NULL,"
    "  `sex` enum('M','F') NOT NULL,"
    "  PRIMARY KEY (`student_number`)"
    ") ENGINE=InnoDB")

cnx = mysql.connector.connect(user='root', password='1234', host='127.0.0.1')
cursor = cnx.cursor()


def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))

    try:
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print("Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)

    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    cursor.close()
    cnx.close()

if __name__ == '__main__':
    create_database(cursor)
    main()




