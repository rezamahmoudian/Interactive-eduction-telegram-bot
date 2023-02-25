import logging
import telegram
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import ConversationHandler
from database.user_db import *
from database.admin_db import get_student_fname, get_student_lname

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

STUDENT_NUMBER, FNAME, LNAME, SEX, PASSWORD, CHECKPASSWORD, CONFIRMATION, CANCEl = range(8)

reply_keyboard = [['شروع دوباره', 'مورد تایید است']]
reply_keyboard_sex = [['زن', 'مرد']]
markup_sex = ReplyKeyboardMarkup(reply_keyboard_sex, resize_keyboard=True, one_time_keyboard=True)
markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)

TOKEN = "5806507050:AAFVm2zmYpAxDwjQtXr_MaROnYM_eZG8gwI"
bot = telegram.Bot(token=TOKEN)


async def start(update, context):
    user = update.message.from_user
    text = update.message.text
    if check_telegram_id_exist(user.id) and check_log(user.id):
        await update.message.reply_text("شما قبلا وارد حساب کاربری خود شده اید \n"
                                        "اگر میخواهید از حساب خود خارج شوید دستور /logout را وارد کنید")
        return ConversationHandler.END
    elif check_telegram_id_exist(user.id) or text == "/login":
        await update.message.reply_text("برای ورود شماره دانشجویی خود را وارد کنید!")
        return STUDENT_NUMBER
    else:
        await update.message.reply_text(
            "سلام من ربات مدیریت کلاس برنامه سازی پیشرفته هستم.اگه میخوای توی این کلاس شرکت کنی شماره دانشجوییت رو "
            "برام بنویس")
        return STUDENT_NUMBER


async def student_number(update, context):
    user = update.message.from_user
    user_data = context.user_data
    category = 'شماره دانشجویی'
    text = update.message.text
    user_data[category] = text
    logger.info("student number of %s: %s", user.first_name, update.message.text)
    try:
        if check_student_number(int(text)):
            if check_student_data(int(text)):
                await update.message.reply_text("برای ورود رمز ورود را بنویسید")
                return CHECKPASSWORD
            else:
                await update.message.reply_text("شماره دانشجویی شما ثبت شده است.")
                await update.message.reply_text("ولی متاسفانه هنوز مشخصاتتان را تکمیل نکرده اید لطفا مشخصات خود را ثبت "
                                                "کنید.")
                await update.message.reply_text("نام خود را وارد کنید:")
                return FNAME
        else:
            await update.message.reply_text("شماره دانشجویی شما در کلاس ثبت نیست.")
            await update.message.reply_text("اگر از دانشجویان کلاس هستید این موصوع را با ta در میان بگذارید.")
            await update.message.reply_text("و یا شماره دانشجویی صحیح را وارد کنید:")
            return STUDENT_NUMBER
    except:
        await update.message.reply_text("لطفا شماره دانشجویی خود را بطور صحیح وارد کنید")
        await update.message.reply_text("برای خروج دستور /cancel را وارد کنید")
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


async def sex(update, context):
    user = update.message.from_user
    user_data = context.user_data
    category = 'جنسیت'
    text = update.message.text
    user_data[category] = text
    logger.info("sex of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text("لطفا برای اکانت خود یک پسوورد انتخاب کنید:", reply_markup=ReplyKeyboardRemove())
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
    check = check_password_from_db(int(student_num), text)
    logger.info("password of %s: %s checked", user.first_name, update.message.text)
    if check:
        # try:
        fname = get_student_fname(int(student_num))
        lname = get_student_lname(int(student_num))
        login(student_num)
        await update.message.reply_text(f"{fname} {lname} شما با موفقیت وارد شدید")
        # except:
        #     login(student_num)
        #     await update.message.reply_text("با موفقیت وارد شدید.")
        #     return ConversationHandler.END
    else:
        await update.message.reply_text("رمز ورود صحیح نیست. لطفا دوباره سعی کنید.")
        await update.message.reply_text("اگر رمز ورود خود را فراموش کرده اید این موضوع را با ta درس درمیان بگذارید. "
                                        "در غیر این صورت رمز عبور صحیح را وارد کنید\n"
                                        "برای خروج از دستور /cancel استفاده کنید")
        return CHECKPASSWORD


async def confirmation(update, context):
    user = update.message.from_user
    user_data = context.user_data
    logger.info("User %s added to the class", user.first_name)
    add_student(user.id, user_data)
    await update.message.reply_text("اطلاعات شما ثبت شد!", reply_markup=ReplyKeyboardRemove())
    await update.message.reply_text("برای ورود شماره دانشجویی خود را وارد کنید:",  reply_markup=ReplyKeyboardRemove())
    return STUDENT_NUMBER


async def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the coneversation", user.first_name)
    await update.message.reply_text("با موفقیت خارج شدید", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


async def logout(update, context):
    user = update.message.from_user
    logout_db(user.id)
    await update.message.reply_text("با موفقیت از حساب کاربری خود خارج شدید")


def facts_to_str(user_data):
    facts = list()
    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))
    return "\n".join(facts).join(['\n', '\n'])
