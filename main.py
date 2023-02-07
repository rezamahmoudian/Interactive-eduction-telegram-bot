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

STUDENT_NUMBER, FNAME, LNAME, SEX, PASSWORD, CHECKPASSWORD, CONFIRMATION = range(7)

TOKEN = "5806507050:AAFVm2zmYpAxDwjQtXr_MaROnYM_eZG8gwI"
bot = telegram.Bot(token=TOKEN)

PORT = int(os.environ.get('PORT', 5000))

reply_keyboard = [['شروع دوباره', 'مورد تایید است']]
reply_keyboard_sex = [['زن', 'مرد']]
markup_sex = ReplyKeyboardMarkup(reply_keyboard_sex, resize_keyboard=True, one_time_keyboard=True)
markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)


async def start(update, context):
    user = update.message.from_user
    user_data = context.user_data
    text = update.message.text
    print(text)

    if check_telegram_id_exist(user.id) and check_log(user.id):
        await update.message.reply_text("با موفقیت وارد شدید!")
        return ConversationHandler.END
    elif check_telegram_id_exist(user.id) or text == "/login":
        await update.message.reply_text("برای ورود شماره دانشجویی خود را وارد کنید!")
        return STUDENT_NUMBER
    else:
        await update.message.reply_text(
            "سلام من ربات مدیریت کلاس برنامه سازی پیشرفته هستم.اگه میخوای توی این کلاس شرکت کنی شماره دانشجوییت رو "
            "برام بنویس")

        return STUDENT_NUMBER


# async def login(update, context):
#     user = update.message.from_user
#     user_data = context.user_data
#
#     await update.message.reply_text("برای ورود شماره دانشجویی خود را وارد کنید!")
#     return STUDENT_NUMBER



def login(student_num):
    cnx = mysql.connector.connect(user='root', password='1234', database='telegram_bot')
    cursor = cnx.cursor()

    query = "UPDATE `telegram_bot`.`students` SET login = 1 WHERE student_number = %d" % int(student_num)
    print(query)
    cursor.execute(query)
    cnx.commit()

    cursor.close()
    cnx.close()


async def logout(update, context):
    user = update.message.from_user
    user_data = context.user_data

    cnx = mysql.connector.connect(user='root', password='1234', database='telegram_bot')
    cursor = cnx.cursor()

    query = "UPDATE `telegram_bot`.`students` SET login = 0 WHERE id = %d" % user.id
    print(query)
    await update.message.reply_text("با موفقیت از حساب کاربری خود خارج شدید")
    cursor.execute(query)
    cnx.commit()

    cursor.close()
    cnx.close()


def check_log(user_id):
    cnx = mysql.connector.connect(user='root', password='1234', database='telegram_bot')
    cursor = cnx.cursor()

    check = False
    query = "SELECT login FROM students WHERE id = %d" % user_id
    cursor.execute(query)
    for data in cursor:
        if data[0] == 1:
            check = True
        else:
            check = False

    cursor.close()
    cnx.close()
    return check


def check_telegram_id_exist(user_id):
    cnx = mysql.connector.connect(user='root', password='1234', database='telegram_bot')
    cursor = cnx.cursor()

    check = False
    query = "SELECT id FROM students"
    cursor.execute(query)
    for data in cursor:
        for id in data:
            print(id)
            if id == user_id:
                check = True

    cursor.close()
    cnx.close()
    return check


def check_student_number(student_number):
    cnx = mysql.connector.connect(user='root', password='1234', database='telegram_bot')
    cursor = cnx.cursor()

    check = False
    query = "SELECT student_number FROM students"
    cursor.execute(query)
    for data in cursor:
        for student_num in data:
            print(student_num)
            if student_num == student_number:
                check = True

    cursor.close()
    cnx.close()
    return check


def check_student_data(student_num):
    cnx = mysql.connector.connect(user='root', password='1234', database='telegram_bot')
    cursor = cnx.cursor()

    check = False
    query = ("SELECT id FROM students WHERE student_number = %d" % student_num)
    cursor.execute(query)
    for data in cursor:
        for id in data:
            print(id)
            if id != -1:
                check = True

    cursor.close()
    cnx.close()
    return check


def check_password_from_db(student_num, password):
    cnx = mysql.connector.connect(user='root', password='1234', database='telegram_bot')
    cursor = cnx.cursor()

    check = False
    query = ("SELECT password FROM students WHERE student_number = {}".format(student_num))
    print(query)
    cursor.execute(query)
    for data in cursor:
        for p in data:
            print(id)
            if p == password:
                check = True

    cursor.close()
    cnx.close()
    return check


async def student_number(update, context):
    user = update.message.from_user
    user_data = context.user_data
    category = 'شماره دانشجویی'
    text = update.message.text
    user_data[category] = text

    logger.info("student number of %s: %s", user.first_name, update.message.text)

    if check_student_number(int(text)):
        if check_student_data(int(text)):
            # await update.message.reply_text("ایول اطلاعاتت رو هم ک قبلا ثبت کردی.")
            await update.message.reply_text("برای ورود رمز ورود رو بنویس")
            return CHECKPASSWORD
        else:
            await update.message.reply_text("شماره دانشجویی شما ثبت شده است.")
            await update.message.reply_text("ولی متاسفانه هنوز مشخصاتتان را تکمیل نکرده اید لطفا مشخصات خود را ثبت "
                                            "کنید.")
            await update.message.reply_text("نام خود را وارد کنید:")
            return FNAME
    else:
        await update.message.reply_text("شماره دانشجویی شما در کلاس ثبت نیست.")
        await update.message.reply_text("لطفا شماره دانشجویی صحیح را وارد کنید.")
        await update.message.reply_text("اگر از دانشجویان کلاس هستید این موصوع را با ta در میان بگذارید.")
        return STUDENT_NUMBER


async def fname(update, context):
    user = update.message.from_user
    user_data = context.user_data
    category = 'نام'
    text = update.message.text
    user_data[category] = text

    logger.info("first name of %s: %s", user.first_name, update.message.text)

    await update.message.reply_text("بسیار عالی")
    await update.message.reply_text("حالا نام خانوادگی خود را وارد کنید:")

    return LNAME


async def lname(update, context):
    user = update.message.from_user
    user_data = context.user_data
    category = 'نام خانوادگی'
    text = update.message.text
    user_data[category] = text

    logger.info("last name of %s: %s", user.first_name, update.message.text)

    await update.message.reply_text("جنسیت خودت رو انتخاب کن.", reply_markup=markup_sex)

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

    await update.message.reply_text("بسیار عالی؛ حالا ی پسوورد برای اکانتت انتخاب کن.")

    return PASSWORD


async def password(update, context):
    user = update.message.from_user
    user_data = context.user_data
    category = 'رمز ورود'

    text = update.message.text
    user_data[category] = text

    logger.info("password of %s: %s", user.first_name, update.message.text)

    await update.message.reply_text(
        'از این که اطلاعات را برای ما ارسال کردین سپاس گزاریم . لطفا بررسی کنید که آیا اطلاعات مورد تاییدتان است یا '
        'نه {}'.format(
            facts_to_str(user_data)),
        reply_markup=markup)

    return CONFIRMATION


async def check_password(update, context):
    user = update.message.from_user
    user_data = context.user_data

    text = update.message.text
    student_num = user_data['شماره دانشجویی']
    print("student num for check password: " + str(student_num))

    check = check_password_from_db(student_num, text)
    logger.info("password of %s: %s checked", user.first_name, update.message.text)
    if check:
        await update.message.reply_text("با موفقیت وارد شدید.")
        login(student_num)
        return ConversationHandler.END
    else:
        await update.message.reply_text("رمز ورود صحیح نیست. لطفا دوباره سعی کنید.")
        await update.message.reply_text("اگر رمز ورود خود را فراموش کرده اید این موضوع را با ta درس درمیان بگذارید. "
                                        "در غیر این صورت رمز عبور صحیح را وارد کنید:")
        return CHECKPASSWORD


async def confirmation(update, context):
    user = update.message.from_user
    user_data = context.user_data
    logger.info("User %s added to the class", user.first_name)

    add_student(user.id, user_data)

    await update.message.reply_text("اطلاعات شما ثبت شد!", reply_markup=ReplyKeyboardRemove())
    await update.message.reply_text("برای ورود شماره دانشجوییت رو وارد کن!")

    return STUDENT_NUMBER


async def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the coneversation", user.first_name)

    await update.message.reply_text("بدرود امیدوارم بازم شما رو ببینم", reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def add_student(user_id, user_data):
    items = []
    for key, value in user_data.items():
        items.append(value)
    print(items)
    if items[3] == 'مرد':
        sex = 'M'
    elif items[3] == 'زن':
        sex = 'F'

    # add user to the database
    cnx = mysql.connector.connect(user='root', password='1234', database='telegram_bot')
    cursor = cnx.cursor()

    update_student = ("UPDATE students"
                      " SET id = %s, first_name = %s, last_name = %s, sex = %s, password = %s"
                      "WHERE student_number = %s")
    print(update_student)
    # add_student = ("INSERT INTO students "
    #                "(id, student_number, first_name, last_name, sex)"
    #                "VALUES (%s, %s, %s, %s, %s)")

    data_student = (user_id, items[1], items[2], sex, items[4], items[0])
    print("262_ ", data_student)
    cursor.execute(update_student, data_student)
    cnx.commit()

    cursor.close()
    cnx.close()


def main():
    app = ApplicationBuilder().token("5806507050:AAFVm2zmYpAxDwjQtXr_MaROnYM_eZG8gwI").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start), CommandHandler('login', start)],

        states={
            STUDENT_NUMBER: [CommandHandler('start', start),CommandHandler('login', start), MessageHandler(filters.TEXT, student_number)],
            FNAME: [CommandHandler('start', start), CommandHandler('login', start), MessageHandler(filters.TEXT, fname)],
            LNAME: [CommandHandler('start', start), CommandHandler('login', start), MessageHandler(filters.TEXT, lname)],
            SEX: [CommandHandler('start', start), CommandHandler('login', start), MessageHandler(filters.TEXT, sex)],
            PASSWORD: [CommandHandler('start', start), CommandHandler('login', start), MessageHandler(filters.TEXT, password)],
            CHECKPASSWORD: [CommandHandler('start', start), CommandHandler('login', start), MessageHandler(filters.TEXT, check_password)],
            CONFIRMATION: [CommandHandler('start', start),CommandHandler('login', start),
                           MessageHandler(filters.Regex('^مورد تایید است$'), confirmation),
                           MessageHandler(filters.Regex('^شروع دوباره$'), start)]
        },

        fallbacks=[CommandHandler('cancle', cancel)]
    )

    # login = CommandHandler(
    #     entry_points=[CommandHandler('login', login)],
    #
    #     states={
    #
    #     }
    # )

    # app.run_webhook(listen='0.0.0.0', port=PORT, url_path=TOKEN)
    # telegram.Bot.set_webhook('https://cb7921f3.ngrok.io/' + TOKEN)

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler('logout', logout))
    app.run_polling()


DB_NAME = 'telegram_bot'
TABLES = {}
TABLES['students'] = (
    "CREATE TABLE `students` ("
    "  `id` int(11) NOT NULL,"
    "  `student_number` int(8) NOT NULL,"
    "  `first_name` varchar(14) NOT NULL,"
    "  `last_name` varchar(16) NOT NULL,"
    "  `password` varchar(20) NOT NULL,"
    "  `sex` enum('M','F') NOT NULL,"
    "  `login` int(2) NOT NULL,"
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
