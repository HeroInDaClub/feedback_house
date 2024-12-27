from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, CallbackQueryHandler, filters

TOKEN = '7037777995:AAEI5HE1Q6zlNVrDbIT-g_lT11zqVxHu5cI'
ADMIN_ID = '5540508943'
FEEDBACK = 1
user_state = {}

async def start(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("Оставить отзыв", callback_data='leave_feedback')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Хотите оставить отзыв?", reply_markup=reply_markup)

async def leave_feedback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    user_state[chat_id] = FEEDBACK
    await query.edit_message_text(text="Отлично! Напишите ваш отзыв, и я передам его администратору.")

async def collect_feedback(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if chat_id in user_state and user_state[chat_id] == FEEDBACK:
        feedback = update.message.text
        await context.bot.send_message(chat_id=ADMIN_ID,
                                       text=f"Новый отзыв от {update.message.from_user.first_name} ({update.message.from_user.username}):\n\n{feedback}")
        await update.message.reply_text("Спасибо за отзыв! Мы его получили.")
        user_state[chat_id] = None

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(leave_feedback, pattern='leave_feedback'))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, collect_feedback))
    application.run_polling()

if __name__ == '__main__':
    main()
