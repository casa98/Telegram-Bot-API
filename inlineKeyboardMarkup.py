from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext.updater import Updater
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
from telegram.callbackquery import CallbackQuery
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update
from telegram.message import Message
import sys
from auth import token

# creating updater
updater: Updater = Updater(token=token, use_context=True)


def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    sys.stderr.write("ERROR: '%s' caused by '%s'" % context.error, update)
    pass


def start(update: Update, context: CallbackContext):
    """
    callback method handling /start command
    """

    # creating list of input buttons
    # documentation: https://python-telegram-bot.readthedocs.io/en/stable/telegram.inlinekeyboardbutton.html
    keyboard = [
        [
        InlineKeyboardButton("Option 1", callback_data='1'),
        InlineKeyboardButton("Option 2", callback_data='2')
        ], 
        [InlineKeyboardButton("Option 3", callback_data='3')]]

    # creating a reply markup of inline keyboard options
    # documentation: https://python-telegram-bot.readthedocs.io/en/stable/telegram.inlinekeyboardmarkup.html
    reply_markup = InlineKeyboardMarkup(keyboard)

    # sending the message to the current chat id
    # documentation: https://python-telegram-bot.readthedocs.io/en/stable/telegram.message.html#telegram.Message.reply_text
    update.message.reply_text('Please choose:', reply_markup=reply_markup)
    pass


def button(update, context):
    """
    callback method handling button press
    """
    # getting the callback query
    # documentation: https://python-telegram-bot.readthedocs.io/en/stable/telegram.callbackquery.html
    query: CallbackQuery = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    # documentation: https://python-telegram-bot.readthedocs.io/en/stable/telegram.callbackquery.html#telegram.CallbackQuery.answer
    query.answer()

    # editing message sent by the bot
    # documentation: https://python-telegram-bot.readthedocs.io/en/stable/telegram.callbackquery.html#telegram.CallbackQuery.edit_message_text
    query.edit_message_text(text="Selected option: {}".format(query.data))


# adding listeners
updater.dispatcher.add_handler(CommandHandler('start', start))  # handling /start command
updater.dispatcher.add_handler(CallbackQueryHandler(button))  # handling inline buttons pressing
updater.dispatcher.add_error_handler(error)  # error handling

# started polling
updater.start_polling()