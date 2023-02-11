from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from main import bot
from database_modules import *

admin_reply_keyboard = [['حذف موضوع', 'افزودن موضوع'],
                        ['حذف همه ی موضوعات', 'نمایش موضوعات'],
                        ['بازگردانی کارتها', 'پخش کارتها', 'ایجاد کارتها'],
                        ['مشاهده ی اطلاعات کاربران']]
confirm_keyboard = [['خیر', 'بله']]
reply_keyboard_broadcast = [['زیرگروه ها', 'سرگروه ها']]
admin_markup = ReplyKeyboardMarkup(admin_reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
confirm_markup = ReplyKeyboardMarkup(confirm_keyboard, resize_keyboard=True, one_time_keyboard=True)
broadcast_markup = ReplyKeyboardMarkup(reply_keyboard_broadcast, resize_keyboard=True, one_time_keyboard=True)

CHECKADMINPASS, CHOOSEACTION, ADDSUB, DELETESUB, SHOWSUBJECTS, DELETEALLSUBJECTS, CREATECARDS, BROADCASTCARDS, RETURNCARDS, SHOWUSERINFORMATION = range(
    10)


async def admin(update, context):
    user = update.message.from_user
    user_data = context.user_data
    text = update.message.text
    print(text)

    await update.message.reply_text("رمز ورود به عنوان ادمین را وارد کنید:")
    return CHECKADMINPASS


admin_pass = "1234"


async def check_admin_pass(update, context):
    user = update.message.from_user
    user_data = context.user_data

    text = update.message.text
    check = text == admin_pass
    if check:
        await update.message.reply_text("با موفقیت وارد شدید.", reply_markup=admin_markup)
        return CHOOSEACTION
    else:
        await update.message.reply_text("رمز ورود صحیح نیست. لطفا دوباره سعی کنید.")

        return CHECKADMINPASS


async def choose_action(update, context):
    user = update.message.from_user
    user_data = context.user_data

    text = update.message.text
    if text == 'افزودن موضوع':
        return ADDSUB
    elif text == 'حذف موضوع':
        return DELETESUB
    elif text == 'نمایش موضوعات':
        return SHOWSUBJECTS
    elif text == 'حذف همه ی موضوعات':
        return DELETEALLSUBJECTS
    elif text == 'ایجاد کارتها':
        await update.message.reply_text("آیا از انجام این فرایند مطمئن هستید؟", reply_markup=confirm_markup)
        return CREATECARDS
    elif text == 'پخش کارتها':
        await update.message.reply_text("قصد پخش کدام دسته از کارتها را دارید؟", reply_markup=broadcast_markup)
        return BROADCASTCARDS
    elif text == 'بازگردانی کارتهای پخش شده':
        return RETURNCARDS
    elif text == 'مشاهده ی اطلاعات کاربران':
        return SHOWUSERINFORMATION
    else:
        await update.message.reply_text("لطفا دستور صحیح را وارد کنید.")
        return CHOOSEACTION


async def create_card_cancel(update, context):
    await update.message.reply_text("ایجاد کارتها لغو شد!", reply_markup=admin_markup)
    return CHOOSEACTION


async def add_cards_db(update, context):
    cnx = database_connector()
    cursor = cnx.cursor()
    delete_leader_cards = "DELETE FROM leader_cards WHERE id != 0;"
    cursor.execute(delete_leader_cards)

    cursor = cnx.cursor()
    delete_cards = "DELETE FROM cards1 WHERE id != 0;"
    cursor.execute(delete_cards)
    cnx.commit()
    cursor.close()
    cards = create_cards()
    cursor = cnx.cursor()
    for data in cards:
        for i in range(len(data) - 1):
            add_card = "INSERT INTO `telegram_bot`.`cards1`(`student_id`,`subject_id`) VALUES " \
                       "({student_id},{subject_id})".format(student_id=data[i + 1], subject_id=data[0])
            print(add_card)
            cursor.execute(add_card)
            cursor = cnx.cursor()
    cnx.commit()
    cursor.close()
    database_disconect(cnx)
    await update.message.reply_text("کارتها با موفقیت در دیتابیس ایجاد شدند.", reply_markup=admin_markup)
    return CHOOSEACTION


async def broadcast_leader_cards(update, context):
    leader_nums = get_leader_nums()
    for student_number in leader_nums:
        first_name = get_student_fname(student_number)
        last_name = get_student_lname(student_number)
        chat_id = get_student_chat_id(student_number)
        topic = get_leader_topic(student_number)
        description = get_leader_description(student_number)

        text = " \n سلام {fname} {lname} عزیز با شماره دانشجویی {student_num}" \
               "\n شما در جلسه ی آینده به عنوان سرگروه انتخاب شده اید" \
               " \n.میباشد {top} موضوع گروه شما در جلسه ی آینده " \
               "\n{descrip} :توضیحات".format(fname=first_name, lname=last_name, student_num=student_number, top=topic,
                                             descrip=description)
        print(text)
        try:
            await bot.send_message(chat_id=chat_id, text=text)
        except:
            print("chat with id %d not fount" % chat_id)
    await update.message.reply_text("کارتهای سرگروه ها با موفقیت پخش شدند.", reply_markup=admin_markup)
    return CHOOSEACTION


async def broadcast_cards(update, context):
    student_nums = get_student_nums()
    for student_number in student_nums:
        subject_id = get_subject_id(student_number)
        first_name = get_student_fname(student_number)
        last_name = get_student_lname(student_number)
        chat_id = get_student_chat_id(student_number)
        topic = get_subject_topic(subject_id)
        description = get_subject_description(subject_id)
        title = get_subject_title(subject_id)

        text = " \n سلام {fname} {lname} عزیز با شماره دانشجویی {student_num}" \
               " \n.میباشد {title} موضوع شما در جلسه ی آینده " \
               "\n{descrip} :توضیحات".format(fname=first_name, lname=last_name, student_num=student_number, title=title,
                                             descrip=description)
        print(text)
        try:
            await bot.send_message(chat_id=chat_id, text=text)
        except:
            print("chat with id %d not fount" % chat_id)
    await update.message.reply_text("کارتها ها با موفقیت پخش شدند.", reply_markup=admin_markup)
    return CHOOSEACTION


if __name__ == '__main__':
    get_subject_topic(6)
