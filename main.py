from __future__ import print_function
from telegram.ext import (CommandHandler, MessageHandler, filters, ApplicationBuilder)
import os
from users import *
from admin import *
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

bot = telegram.Bot(token=TOKEN)

PORT = int(os.environ.get('PORT', 5000))


async def help(update, context):
    user = update.message.from_user
    user_data = context.user_data
    await update.message.reply_text("با استفاده از کلید menu میتوانید لیست دستورات را مشاهده کنید.\n"
                                    "با ارسال هریک از دستورات وارد یک مکالمه با ربات میشوید.\n"
                                    "**لطفا قبل از پایان هر مکالمه دستور دیگری وارد نکنید** \n"
                                    "شما میتوانید در هر لحظه با استفاده از دستور /cancle مکالمه ی خود با ربات را به "
                                    "پایان برسانید. \n "
                                    "با دستور /start ربات آغاز ب کار میکند\n"
                                    "با دستور /login شما میتوانید وارد حساب کاربری خود شوید.\n"
                                    "با دستور /logout از حساب کاربری خود خارج میشوید.\n"
                                    "دستور /admin برای ورود ب ربات به عنوان مدیر است.\n")


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start), CommandHandler('login', start)],

        states={
            STUDENT_NUMBER: [CommandHandler('start', start), CommandHandler('login', start),
                             CommandHandler('cancle', cancle),
                             MessageHandler(filters.TEXT, student_number)],
            FNAME: [CommandHandler('start', start), CommandHandler('login', start), CommandHandler('cancle', cancle),
                    MessageHandler(filters.TEXT, fname)],
            LNAME: [CommandHandler('start', start), CommandHandler('login', start), CommandHandler('cancle', cancle),
                    MessageHandler(filters.TEXT, lname)],
            SEX: [CommandHandler('start', start), CommandHandler('login', start), CommandHandler('cancle', cancle),
                  MessageHandler(filters.TEXT, sex)],
            PASSWORD: [CommandHandler('start', start), CommandHandler('login', start), CommandHandler('cancle', cancle),
                       MessageHandler(filters.TEXT, password)],
            CHECKPASSWORD: [CommandHandler('start', start), CommandHandler('login', start),
                            CommandHandler('cancle', cancle),
                            MessageHandler(filters.TEXT, check_password)],
            CONFIRMATION: [CommandHandler('start', start), CommandHandler('login', start),
                           CommandHandler('cancle', cancle),
                           MessageHandler(filters.Regex('^مورد تایید است$'), confirmation),
                           MessageHandler(filters.Regex('^شروع دوباره$'), start)],
        },

        fallbacks=[CommandHandler('cancle', cancle)]
    )
    admin_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('admin', admin)],
        states={
            CHECKADMINPASS: [CommandHandler('admin', admin), CommandHandler('cancle', cancle),
                             MessageHandler(filters.TEXT, check_admin_pass)],
            # CHOOSEACTION: [CommandHandler('admin', admin),
            #                MessageHandler(filters.Regex('^ایجاد کارتها$'), add_cards_db),
            #                MessageHandler(filters.Regex('^پخش کارتها$'), broadcast_cards),
            #                ]
            CHOOSEACTION: [CommandHandler('admin', admin), CommandHandler('cancle', cancle),
                           MessageHandler(filters.TEXT, choose_action),
                           ],
            CREATECARDS: [CommandHandler('admin', admin), CommandHandler('cancle', cancle),
                          MessageHandler(filters.Regex('^بله$'), add_cards_db),
                          MessageHandler(filters.Regex('^خیر'), create_card_cancel),
                          ],
            BROADCASTCARDS: [CommandHandler('admin', admin), CommandHandler('cancle', cancle),
                             MessageHandler(filters.Regex('^سرگروه ها$'), broadcast_leader_cards),
                             MessageHandler(filters.Regex('^زیرگروه ها'), broadcast_cards),
                             ]
        },
        fallbacks=[CommandHandler('cancle', cancle)]
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler('logout', logout))
    app.add_handler(CommandHandler('help', help))
    app.add_handler(admin_conv_handler)

    app.run_polling()


if __name__ == '__main__':
    create_database()
    main()
