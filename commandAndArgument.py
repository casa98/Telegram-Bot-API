from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler
from auth import token
import telegram
import logging
from telegram.ext.filters import Filters

updater = Updater(token=token, use_context=True)

job = updater.job_queue

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update, context):
    print(update.effective_chat.id)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, "+update.message.from_user.first_name +"!")

def caps(update, context):
    # context.arg is the message passed along with /caps command, e.g: /caps Soy del verde, soy feliz
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


def inline_caps(update, context):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title=query.upper(),
            description='Returns text in Capital Letter',
            thumb_url='https://cdn4.iconfinder.com/data/icons/education-flat-9/614/1070_-_Upercase-512.png',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    results.append(
        InlineQueryResultArticle(
            id=query.lower(),
            title=query.lower(),
            description='Returns text in Lower Case',
            thumb_url='https://cdn4.iconfinder.com/data/icons/education-flat-9/614/1071_-_Lowercase-512.png',
            input_message_content=InputTextMessageContent(query.lower())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)


def callback_minute(context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id='@fanzinemedia', text='Mama quéeeeeeeeeeeee\nMoto?')


job_minute = job.run_repeating(callback_minute, interval=30, first=0)


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)

inline_caps_handler = InlineQueryHandler(inline_caps)
dispatcher.add_handler(inline_caps_handler)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()
updater.idle()
