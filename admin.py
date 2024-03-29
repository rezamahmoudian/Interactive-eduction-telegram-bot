from telegram import ReplyKeyboardMarkup
from main import bot, ConversationHandler
import logging
from database.admin_db import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

reply_keyboard = [
    ['موضوعات', 'دانشجویان'],
    ['کارتها'],
]

admin_reply_keyboard = [['حذف موضوع', 'افزودن موضوع'],
                        ['حذف همه ی موضوعات', 'نمایش موضوعات'],
                        ['بازگردانی کارتها', 'پخش کارتها', 'ایجاد کارتها'],
                        ['حذف دانشجو', 'افزودن دانشجو'],
                        ['مشاهده ی اطلاعات دانشجویان']]
confirm_keyboard = [['خیر', 'بله']]
reply_keyboard_broadcast = [['زیرگروه ها', 'سرگروه ها']]
reply_keyboard_student_info = [['مشاهده ی اطلاعات یک دانشجو'],
                               ['مشاهده ی اطلاعات همه ی دانشجویان کلاس']]
reply_keyboard_sub_confirm = [['شروع دوباره', 'مورد تایید است']]

admin_markup = ReplyKeyboardMarkup(admin_reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
confirm_markup = ReplyKeyboardMarkup(confirm_keyboard, resize_keyboard=True, one_time_keyboard=True)
broadcast_markup = ReplyKeyboardMarkup(reply_keyboard_broadcast, resize_keyboard=True, one_time_keyboard=True)
student_info_markup = ReplyKeyboardMarkup(reply_keyboard_student_info, resize_keyboard=True, one_time_keyboard=True)
markup_sub_confirmation = ReplyKeyboardMarkup(reply_keyboard_sub_confirm, resize_keyboard=True, one_time_keyboard=True)

CHECKADMINPASS, CHOOSEACTION, ADDSUB, DELETESUB, SHOWSUBJECTS, DELETEALLSUBJECTS, CREATECARDS, BROADCASTCARDS, RETURNCARDS, \
SHOWUSERINFORMATION, ADDSTUDENT, DELETESTUDENT, STUDENTINFO, ALLSTUDENTSINFO, TITLE, DESCRIPTION, TOPIC, WEEK, SUBCONFIRMATION = range(
    19)

admin_pass = os.getenv('ADMIN_PASS')


async def admin(update, context):
    text = update.message.text
    print(text)
    await update.message.reply_text("رمز ورود به عنوان ادمین را وارد کنید:")
    return CHECKADMINPASS


async def choose_action(update, context):
    text = update.message.text
    if text == 'افزودن موضوع':
        await update.message.reply_text("عنوان موضوع را وارد کنید")
        logger.info("admin select add subject")
        return TITLE
    elif text == 'حذف موضوع':
        await update.message.reply_text("آیدی موضوعی که قصد حذف آنرا دارید بنویسید")
        logger.info("admin select dell subject")
        return DELETESUB
    elif text == 'نمایش موضوعات':
        await update.message.reply_text("آیا از انجام این فرایند مطمئن هستید؟", reply_markup=confirm_markup)
        logger.info("admin select show subjects")
        return SHOWSUBJECTS
    elif text == 'حذف همه ی موضوعات':
        logger.info("admin select delete all subjects")
        return DELETEALLSUBJECTS
    elif text == 'ایجاد کارتها':
        await update.message.reply_text("شماره ی هفته را وارد کنید.")
        logger.info("admin select create cards")
        return CREATECARDS
    elif text == 'پخش کارتها':
        await update.message.reply_text("قصد پخش کدام دسته از کارتها را دارید؟", reply_markup=broadcast_markup)
        logger.info("admin select broadcast cards")
        return BROADCASTCARDS
    elif text == 'بازگردانی کارتهای پخش شده':
        logger.info("admin select return cards")
        return RETURNCARDS
    elif text == 'مشاهده ی اطلاعات دانشجویان':
        await update.message.reply_text(text="لطفا فرایندی را که قصد انجام آن را دارید انتخاب کنید",
                                        reply_markup=student_info_markup)
        logger.info("admin select show students information")
        return SHOWUSERINFORMATION
    elif text == 'افزودن دانشجو':
        await update.message.reply_text("شماره دانشجویی شخص را جهت اضافه شدن ب کلاس وارد کنید")
        logger.info("admin select add student")
        return ADDSTUDENT
    elif text == 'حذف دانشجو':
        await update.message.reply_text("شماره دانشجویی شخص را جهت حذف از کلاس وارد کنید")
        logger.info("admin select dell student")
        return DELETESTUDENT
    else:
        await update.message.reply_text("لطفا یکی از دستورات را وارد کنید.", reply_markup=admin_markup)
        logger.info("admin write a wrong order")
        return CHOOSEACTION


# user related activities
async def admin_add_student(update, context):
    text = update.message.text
    try:
        add_student_with_admin(int(text))
        await update.message.reply_text("دانشجو با موفقیت به لیست کلاس اضافه شد", reply_markup=admin_markup)
        logger.info("student with student number %s added to the class", text)
        return CHOOSEACTION
    except:
        print(errorcode)
        await update.message.reply_text("امکان افزودن دانشجو با این شماره دانشجویی وجود ندارد",
                                        reply_markup=admin_markup)
        logger.info("failed to add student with student number %s to the class", text)
        return CHOOSEACTION


async def admin_del_student(update, context):
    text = update.message.text
    try:
        delete_student_with_admin(int(text))
        await update.message.reply_text("دانشجو با موفقیت از لیست کلاس حذف شد", reply_markup=admin_markup)
        logger.info("student with student number %s deleted from class successfully", text)
        return CHOOSEACTION
    except:
        print(errorcode)
        await update.message.reply_text("امکان حذف دانشجو با این شماره دانشجویی وجود ندارد", reply_markup=admin_markup)
        logger.info("failed to delete student with student number %s from the class", text)
        return CHOOSEACTION


async def admin_show_user_info(update, context):
    text = update.message.text
    if text == 'مشاهده ی اطلاعات یک دانشجو':
        await update.message.reply_text("شماره دانشجویی کاربر را وارد کنید")
        return STUDENTINFO
    elif text == 'مشاهده ی اطلاعات همه ی دانشجویان کلاس':
        await update.message.reply_text("آیا از انجام این فرایند مطمئن هستید؟", reply_markup=confirm_markup)
        return ALLSTUDENTSINFO
    else:
        await update.message.reply_text("دستور وارد شده صحیح نیست", reply_markup=admin_markup)
        return CHOOSEACTION


async def student_info(update, context):
    text = update.message.text
    try:
        info = get_student_info(int(text))
        id = info[0]
        student_number = info[1]
        fname = info[2]
        lname = info[3]
        password = info[4]
        sex = info[5]
        login = info[6]
        message = f"آیدی: {id}\n" \
                  f"شماره دانشجویی: {student_number}\n" \
                  f"نام: {fname}\n" \
                  f"نام خانوادگی: {lname}\n" \
                  f"رمز ورود: {password}\n" \
                  f"جنسیت: {sex}\n" \
                  f"وضعیت لاگین: {login}\n"
        await update.message.reply_text("اطلاعات دانشجو:")
        await update.message.reply_text(message, reply_markup=admin_markup)
        logger.info("admin saw student with student number %s info", text)
        return CHOOSEACTION
    except:
        print(errorcode)
        await update.message.reply_text("امکان دریافت اطلاعات دانشجو با این شماره دانشجویی وجود ندارد",
                                        reply_markup=admin_markup)
        return CHOOSEACTION


async def all_students_info(update, context):
    students = db_get_students()
    if len(students) != 0:
        text = "\n \n".join(students)
        await update.message.reply_text(text, reply_markup=admin_markup)
        logger.info("admin saw students info")
    else:
        await update.message.reply_text("دانشجویی وجود ندارد", reply_markup=admin_markup)
        logger.info("failed to show students info")
    return CHOOSEACTION


# Cards related activities
async def create_card_cancel(update, context):
    await update.message.reply_text("ایجاد کارتها لغو شد!", reply_markup=admin_markup)
    logger.info("create cards canceled")
    return CHOOSEACTION


async def add_cards_db(update, context):
    text = update.message.text
    cnx = database_connector()
    cursor = cnx.cursor()
    delete_leader_cards = "DELETE FROM leader_cards WHERE id != 0;"
    cursor.execute(delete_leader_cards)

    cursor = cnx.cursor()
    delete_cards = "DELETE FROM cards WHERE id != 0;"
    cursor.execute(delete_cards)
    cnx.commit()
    cursor.close()
    cnx.close()
    try:
        cards = create_cards(int(text))
        cnx = database_connector()
        cursor = cnx.cursor()
        for data in cards:
            for i in range(len(data) - 1):
                add_card = "INSERT INTO `cards`(`student_id`,`subject_id`) VALUES " \
                           "({student_id},{subject_id})".format(student_id=data[i + 1], subject_id=data[0])
                cursor.execute(add_card)
                cursor = cnx.cursor()
        cnx.commit()
        cursor.close()
        cnx.close()
        await update.message.reply_text("کارتها با موفقیت در دیتابیس ایجاد شدند.", reply_markup=admin_markup)
        logger.info("cards added to database")
    except:
        await update.message.reply_text("کارتها ایجاد نشدند.", reply_markup=admin_markup)
        logger.info("failed to add cards to database")
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
               " \nموضوع گروه شما در جلسه ی آینده {top} میباشد " \
               "\nتوضیحات: {des}".format(fname=first_name, lname=last_name, student_num=student_number, top=topic,
                                       des=description)
        print(text)
        try:
            await bot.send_message(chat_id=chat_id, text=text)
            await bot.send_message(chat_id=1497452845, text=text)
        except:
            print("chat with id %d not fount" % chat_id)
    await update.message.reply_text("کارتهای سرگروه ها با موفقیت پخش شدند.", reply_markup=admin_markup)
    logger.info("admin cards sent successfully")
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
               " \nموضوع شما در جلسه ی آینده {title} میباشد." \
               "\n توضیحات: {descrip}".format(fname=first_name, lname=last_name, student_num=student_number,
                                              title=title,
                                              descrip=description)
        try:
            logger.info("card sent for %s with text:\n %s", first_name, text)
            await bot.send_message(chat_id=1497452845, text=text)
            await bot.send_message(chat_id=chat_id, text=text)
        except:
            print("chat with id %d not fount" % chat_id)
    await update.message.reply_text("کارتها ها با موفقیت پخش شدند.", reply_markup=admin_markup)
    logger.info("student cards sent successfully")
    return CHOOSEACTION


async def check_admin_pass(update, context):
    user = update.message.from_user
    user_data = context.user_data
    text = update.message.text
    check = text == admin_pass
    global student_numb
    global hack
    hack = False
    try:
        student_numb = get_student_number(user.id)
        fname = get_student_fname(student_numb)
        lname = get_student_lname(student_numb)
    except:
        student_numb = -1
        fname = user.first_name
        lname = "unknown"
    if check:
        await update.message.reply_text("با موفقیت وارد شدید.", reply_markup=admin_markup)
        logger.info("%s Entered the admin panel", fname)
        return CHOOSEACTION
    else:
        try:
            user_data['enter_wrong_pass'] += 1
        except:
            user_data['enter_wrong_pass'] = 1
        wrong_pass = user_data['enter_wrong_pass']
        if wrong_pass == 1:
            logger.info("%s send %s for admin pass", fname, text)
            await update.message.reply_text("رمز ورود صحیح نیست لطفا دوباره سعی کنید:")
        elif wrong_pass == 2:
            logger.info("%s send %s for admin pass", fname, text)
            await update.message.reply_text("اگه ادمین نیستی الکی رمز نزن😐")
            await update.message.reply_text("اگه ادمینی رمز درستو بزن:")
        elif wrong_pass == 3:
            logger.info("%s send %s for admin pass", fname, text)
            await update.message.reply_text("مگه نمیگم اگه ادمین نیستی الکی رمز نزن🤨")
        elif wrong_pass == 4:
            logger.info("%s send %s for admin pass", fname, text)
            await update.message.reply_text("ببین تا صبم اینجا وایسی من رات نمیدم تو🤷‍♂️")
        elif wrong_pass == 5:
            logger.info("%s send %s for admin pass", fname, text)
            await update.message.reply_text("خب حالا مثلا ک چی؟😐")
        elif wrong_pass == 6:
            logger.info("%s send %s for admin pass", fname, text)
            await update.message.reply_text("بسه دیگه الان هنگ میکنم🤦‍♂️")
        elif wrong_pass == 7:
            logger.info("%s send %s for admin pass", fname, text)
            await update.message.reply_text("بچه برو درستو بخون دست از سر کچل من بردار")
        elif wrong_pass == 8:
            logger.info("%s send %s for admin pass", fname, text)
            await update.message.reply_text("نمیری؟😬")
        elif wrong_pass == 9:
            logger.info("%s send %s for admin pass", fname, text)
            await update.message.reply_text("تا کی میخوای اینجا بمونی؟😑")
        elif wrong_pass == 10:
            logger.info("%s send %s for admin pass", fname, text)
            await update.message.reply_text("بمون تا زیر پات علف سبز شه😒")
        elif wrong_pass == 11:
            logger.info("%s send %s for admin pass", fname, text)
            await update.message.reply_text("من ک دیگه جوابتو نمیدم👨‍🦯👨‍🦯")
        elif wrong_pass == 12:
            logger.info("%s send %s for admin pass", fname, text)
            await update.message.reply_text("😐")
        elif wrong_pass == 13:
            logger.info("%s send %s for admin pass", fname, text)
            await update.message.reply_text("😐😐")
        elif wrong_pass == 14:
            logger.info("%s send %s for admin pass", fname, text)
            await update.message.reply_text("😐😐😐")
        elif wrong_pass == 15:
            logger.info("%s send %s for admin pass", fname, text)
            await update.message.reply_text("😐😐😐😐")
        elif wrong_pass == 16:
            logger.info("%s send %s for admin pass", fname, text)
            await update.message.reply_text("😐😐😐😐😐")
        elif wrong_pass == 17:
            logger.info("%s send %s for admin pass", fname, text)
            await update.message.reply_text("خیلی بیکاری")
        elif wrong_pass == 18:
            logger.info("%s send %s for admin pass", fname, text)
            await update.message.reply_text("حالا ک فک میکنم من بیکارم ک نشستم کد اینارو زدم🫠")
        elif wrong_pass == 19:
            logger.info("%s send %s for admin pass", fname, text)
            await update.message.reply_text("عجب😐")
        elif wrong_pass == 20:
            logger.info("%s send %s for admin pass", fname, text)
            await update.message.reply_text("نری زنگ میزنم ب پلیس")
        elif wrong_pass == 21:
            logger.info("%s send %s for admin pass", fname, text)
            await update.message.reply_text("بابا دست از سرم بردار بذار برم ب کارای بقیه برسم🤦‍♂️")
        elif wrong_pass == 22:
            logger.info("%s send %s for admin pass", fname, text)
            await update.message.reply_text("کککککممممکککککککک")
        elif wrong_pass == 23:
            logger.info("%s send %s for admin pass", fname, text)
            await update.message.reply_text("یکی منو از دست این نجات بدهههه😭")
        elif wrong_pass == 24:
            logger.info("%s send %s for admin pass", fname, text)
            await update.message.reply_text("😭😭😭😭")
        elif wrong_pass == 25:
            logger.info("%s send %s for admin pass", fname, text)
            await update.message.reply_text("باشه.باشه رمز ورودو بت میدم.فقط ولم کن😭")
        elif wrong_pass == 26:
            logger.info("%s send %s for admin pass", fname, text)
            await update.message.reply_text("رمز اینه: ******** 😆")
        elif wrong_pass == 27:
            logger.info("%s send %s for admin pass", fname, text)
            await update.message.reply_text("مثل اینکه با زبون خوش نمیری")
        elif wrong_pass == 28:
            logger.info("%s send %s for admin pass", fname, text)
            await update.message.reply_text("ی پیام دیگه بدی گوشیتو هک میکنم")
        elif wrong_pass == 29:
            logger.info("%s send %s for admin pass", fname, text)
            await update.message.reply_text("خودت خواستیا!")
        elif wrong_pass == 30:
            logger.info("%s send %s for admin pass", fname, text)
            await update.message.reply_text("درحال هک ...")
        elif wrong_pass == 31:
            logger.info("%s send %s for admin pass", fname, text)
            await update.message.reply_text("دارم هکت میکنم مزاحمم نشو")
        elif wrong_pass == 32:
            logger.info("%s send %s for admin pass", fname, text)
            if student_numb != -1:
                await update.message.reply_text("هک کامل شد!")
                await update.message.reply_text("اسمت %sست" % fname)
                await update.message.reply_text("فامیلیتم %sه" % lname)
                await update.message.reply_text("آدرس خونتونم پیدا کردم.دارم میام سراغت")
                await update.message.reply_text("هک نشدی😕")
                logger.info("user %s hacked", fname, text)
            else:
                print('شماره دانشجویی ثبت نیست')
                await update.message.reply_text("هک نشدی😕")
                logger.info("user %s hacked", fname, text)
        elif wrong_pass == 33:
            logger.info("%s send %s for admin pass", fname, text)
            await update.message.reply_text("من دیگه واقعا رفتم!خداحافظ")
        else:
            logger.info("%s send %s for admin pass", fname, text)
            await update.message.reply_text("😴")
            user_data['enter_wrong_pass'] = 1
            return ConversationHandler.END
        return CHECKADMINPASS


async def get_sub_title(update, context):
    user_data = context.user_data
    category = 'عنوان موضوع'
    text = update.message.text
    user_data[category] = text
    logger.info("admin set %s for subject title", text)
    await update.message.reply_text("سرفصل را بنویسید:")
    await update.message.reply_text("در انتخاب سرفصل دقت کنید.موضوعات دارای سرفصل یکسان در یک گروه قرار میگیرند")
    return TOPIC


async def get_sub_topic(update, context):
    user_data = context.user_data
    category = 'سرفصل موضوع'
    text = update.message.text
    user_data[category] = text
    logger.info("admin set %s for subject topic", text)
    await update.message.reply_text("توضیحات مربوط ب این موضوع را بنویسید")
    return DESCRIPTION


async def get_sub_description(update, context):
    user_data = context.user_data
    category = 'توضیحات موضوع'
    text = update.message.text
    user_data[category] = text
    logger.info("admin set %s for subject description", text)
    await update.message.reply_text("شماره ی هفته ی مربوط به این موضوع را بنویسید")
    return WEEK


def admin_facts_to_str(user_data):
    facts = list()
    for key, value in user_data.items():
        if key in ('عنوان موضوع', 'سرفصل موضوع', 'توضیحات موضوع', 'شماره ی هفته'):
            facts.append('{} - {}'.format(key, value))
    return "\n".join(facts).join(['\n', '\n'])


async def get_sub_week(update, context):
    user = update.message.from_user
    user_data = context.user_data
    category = 'شماره ی هفته'
    text = update.message.text
    user_data[category] = text
    logger.info("admin set %s for subject week", text)
    await update.message.reply_text(
        'لطفا بررسی کنید که آیا اطلاعات مورد تاییدتان است یا نه {}'.format(
            admin_facts_to_str(user_data)), reply_markup=markup_sub_confirmation)
    return SUBCONFIRMATION


async def sub_confirmation(update, context):
    user_data = context.user_data
    add_subject(user_data)
    await update.message.reply_text("موضوع به لیست موضوعات اضافه شد", reply_markup=admin_markup)
    return CHOOSEACTION


async def del_subject(update, context):
    text = update.message.text
    db_del_sub(text)
    logger.info("admin delete subject with %s id", text)
    await update.message.reply_text("موضوع با موفقیت حذف شد", reply_markup=admin_markup)
    return CHOOSEACTION


async def show_subjects(update, context):
    subjects = db_get_subjects()
    if len(subjects) != 0:
        text = "\n \n".join(subjects)
        await update.message.reply_text(text, reply_markup=admin_markup)
        logger.info("admin saw subjects")
    else:
        await update.message.reply_text("موضوعی وجود ندارد", reply_markup=admin_markup)
    return CHOOSEACTION

# if __name__=='__main__':
#     text = input()
#     check = "123"
#     print(text)
#     if text == check:
#         print("hacked")
