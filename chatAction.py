from telegram.bot import Bot
from telegram.update import Update
from telegram.ext.updater import Updater
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram.chataction import ChatAction
from time import sleep
from auth import token 

updater = Updater(token=token, use_context=True)

def echo(update: Update, context: CallbackContext):
    # sending the chat action, under the name of bot it will show Typing...
    # documentation: https://python-telegram-bot.readthedocs.io/en/stable/telegram.chataction.html
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    # simulating some long processing
    sleep(3)

    # sending reply when it's done
    update.message.reply_text(text="You sent me '%s'" % update.message.text)


updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))

updater.start_polling()