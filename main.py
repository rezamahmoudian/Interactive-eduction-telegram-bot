from __future__ import print_function
from telegram.ext import (CommandHandler, MessageHandler, filters, ApplicationBuilder, CallbackQueryHandler)
from users import *
from admin import *
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

bot = telegram.Bot(token=TOKEN)

PORT = int(os.environ.get('PORT', 5000))


async def help(update, context):
    await update.message.reply_text("با استفاده از کلید menu میتوانید لیست دستورات را مشاهده کنید.\n"
                                    "با ارسال هریک از دستورات وارد یک مکالمه با ربات میشوید.\n"
                                    "**لطفا قبل از پایان هر مکالمه دستور دیگری وارد نکنید**\n"
                                    "شما میتوانید در هر لحظه با استفاده از دستور /cancel مکالمه ی خود با ربات را به "
                                    "پایان برسانید. \n "
                                    "با دستور /start ربات آغاز ب کار میکند\n"
                                    "با دستور /login شما میتوانید وارد حساب کاربری خود شوید.\n"
                                    "با دستور /logout از حساب کاربری خود خارج میشوید.\n"
                                    "دستور /admin برای ورود ب ربات به عنوان مدیر است.\n")
    return ConversationHandler.END


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start), CommandHandler('login', start)],

        states={
            STUDENT_NUMBER: [CommandHandler('start', start), CommandHandler('login', start),
                             CommandHandler('cancel', cancel), CommandHandler('help', help),
                             MessageHandler(filters.TEXT, student_number)],
            FNAME: [CommandHandler('start', start), CommandHandler('login', start),
                    CommandHandler('cancel', cancel), CommandHandler('help', help),
                    MessageHandler(filters.TEXT, fname)],

            LNAME: [CommandHandler('start', start), CommandHandler('login', start), CommandHandler('cancel', cancel),
                    CommandHandler('help', help), MessageHandler(filters.TEXT, lname)],

            SEX: [CommandHandler('start', start), CommandHandler('login', start), CommandHandler('cancel', cancel),
                  CommandHandler('help', help), MessageHandler(filters.TEXT, sex)],

            PASSWORD: [CommandHandler('start', start), CommandHandler('login', start), CommandHandler('cancel', cancel),
                       CommandHandler('help', help), MessageHandler(filters.TEXT, password)],

            CHECKPASSWORD: [CommandHandler('start', start), CommandHandler('login', start),
                            CommandHandler('cancel', cancel), CommandHandler('help', help),
                            MessageHandler(filters.TEXT, check_password)],

            CONFIRMATION: [CommandHandler('start', start), CommandHandler('login', start),
                           CommandHandler('cancel', cancel), CommandHandler('help', help),
                           MessageHandler(filters.Regex('^مورد تایید است$'), confirmation),
                           MessageHandler(filters.Regex('^شروع دوباره$'), start)],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    admin_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('admin', admin)],
        states={
            ADDSTUDENT: [CommandHandler('admin', admin), CommandHandler('cancel', cancel),
                         MessageHandler(filters.TEXT, admin_add_student),
                         ],
            DELETESTUDENT: [CommandHandler('admin', admin), CommandHandler('cancel', cancel),
                            MessageHandler(filters.TEXT, admin_del_student),
                            ],
            CHECKADMINPASS: [CommandHandler('admin', admin), CommandHandler('cancel', cancel),
                             MessageHandler(filters.TEXT, check_admin_pass)
                             ],
            CHOOSEACTION: [CommandHandler('admin', admin), CommandHandler('cancel', cancel),
                           MessageHandler(filters.TEXT, choose_action),
                           ],
            CREATECARDS: [CommandHandler('admin', admin), CommandHandler('cancel', cancel),
                          MessageHandler(filters.TEXT, add_cards_db),
                          ],
            BROADCASTCARDS: [CommandHandler('admin', admin), CommandHandler('cancel', cancel),
                             MessageHandler(filters.Regex('^سرگروه ها$'), broadcast_leader_cards),
                             MessageHandler(filters.Regex('^زیرگروه ها'), broadcast_cards),
                             ],
            SHOWUSERINFORMATION: [CommandHandler('admin', admin), CommandHandler('cancel', cancel),
                                  MessageHandler(filters.TEXT, admin_show_user_info)
                                  ],
            STUDENTINFO: [CommandHandler('admin', admin), CommandHandler('cancel', cancel),
                          MessageHandler(filters.TEXT, student_info)
                          ],
            ALLSTUDENTSINFO: [CommandHandler('admin', admin), CommandHandler('cancel', cancel),
                              MessageHandler(filters.TEXT, all_students_info)
                              ],
            # add subject
            TITLE: [CommandHandler('admin', admin), CommandHandler('cancel', cancel),
                     MessageHandler(filters.TEXT, get_sub_title)
                    ],
            TOPIC: [CommandHandler('admin', admin), CommandHandler('cancel', cancel),
                    MessageHandler(filters.TEXT, get_sub_topic)
                    ],
            DESCRIPTION: [CommandHandler('admin', admin), CommandHandler('cancel', cancel),
                    MessageHandler(filters.TEXT, get_sub_description)
                          ],
            WEEK: [CommandHandler('admin', admin), CommandHandler('cancel', cancel),
                    MessageHandler(filters.TEXT, get_sub_week)
                   ],
            SUBCONFIRMATION: [CommandHandler('admin', admin), CommandHandler('cancel', cancel),
                              MessageHandler(filters.Regex('^مورد تایید است$'), sub_confirmation),
                              MessageHandler(filters.Regex('^شروع دوباره$'), choose_action)
                              ],
            SHOWSUBJECTS: [CommandHandler('admin', admin), CommandHandler('cancel', cancel),
                           MessageHandler(filters.Regex('^بله$'), show_subjects),
                           MessageHandler(filters.Regex('^خیر'), choose_action),
                           ],
            DELETESUB: [CommandHandler('admin', admin), CommandHandler('cancel', cancel),
                        MessageHandler(filters.TEXT, del_subject)
                        ],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler('logout', logout))
    app.add_handler(CommandHandler('help', help))
    app.add_handler(admin_conv_handler)

    app.run_polling()


if __name__ == '__main__':
    create_database()
    main()
