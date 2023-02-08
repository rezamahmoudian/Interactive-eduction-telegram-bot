# admin_reply_keyboard = [['حذف موضوع', 'افزودن موضوع'],
#                   ['حذف همه ی موضوعات', 'نمایش موضوعات'],
#                   ['بازگردانی کارتهای پخش شده', 'پخش کارتها'],
#                   ['مشاهده ی اطلاعات کاربران']]
# admin_markup = ReplyKeyboardMarkup(admin_reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
#
# CHECKADMINPASS, CHOOSEACTION, ADDSUB, DELETESUB, SHOWSUBJECTS, DELETEALLSUBJECTS, BROADCASTCARDS, RETURNCARDS, SHOWUSERINFORMATION = range(9)
#
#
# async def admin(update, context):
#     user = update.message.from_user
#     user_data = context.user_data
#     text = update.message.text
#     print(text)
#
#     await update.message.reply_text("رمز ورود به عنوان ادمین را وارد کنید:")
#     return CHECKADMINPASS
#
#
# admin_pass = "1234"
#
#
# async def check_admin_pass(update, context):
#     user = update.message.from_user
#     user_data = context.user_data
#
#     text = update.message.text
#     check = text == admin_pass
#     if check:
#         await update.message.reply_text("با موفقیت وارد شدید.", reply_markup=admin_markup)
#         return CHOOSEACTION
#     else:
#         await update.message.reply_text("رمز ورود صحیح نیست. لطفا دوباره سعی کنید.")
#
#         return CHECKPASSWORD
#
#
# async def choose_action(update, context):
#     user = update.message.from_user
#     user_data = context.user_data
#
#     text = update.message.text
#     if text == 'افزودن موضوع':
#         return ADDSUB
#     elif text == 'حذف موضوع':
#         return DELETESUB
#     elif text == 'نمایش موضوعات':
#         return SHOWSUBJECTS
#     elif text == 'حذف همه ی موضوعات':
#         return DELETEALLSUBJECTS
#     elif text == 'پخش کارتها':
#         return BROADCASTCARDS
#     elif text == 'بازگردانی کارتهای پخش شده':
#         return RETURNCARDS
#     elif text == 'مشاهده ی اطلاعات کاربران':
#         return SHOWUSERINFORMATION
#     else:
#         await update.message.reply_text("لطفا دستور صحیح را وارد کنید.")
#         return CHOOSEACTION
#




