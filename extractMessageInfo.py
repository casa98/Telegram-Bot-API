#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from auth import token
from langdetect import detect

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_info(text):
    finalText = ''
    text_words = text.count(' ')
    finalText += "{} words.\n".format(text_words+1)
    text_len = len(text)
    finalText += "{} characters.\n".format(text_len)
    text_vowels = text.lower()
    text_vowels_counter = 0
    text_consonants_counter = 0
    vowels = 'aeiouáéíóú'
    consonants = 'bcdfghjklmnñpqrstvwxyz'
    for i in text_vowels:
        if i in vowels:
            text_vowels_counter += 1
        if i in consonants:
            text_consonants_counter += 1

    finalText += "{} vowels.\n".format(text_vowels_counter)
    finalText += "{} consonants.\n".format(text_consonants_counter)

    if(text_words > 6): # At least 8 words
        lang = detect(text)
        finalText += '\nYour text is probably written in {} language'.format(lang)
    return finalText


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi, '+ update.message.from_user.first_name +'!\nI\'ll extract some info from the messages you send me.\nThe longer the text, the more surprises you get \U0001f609')


def help(bot, update):
    update.message.reply_text('Hi, I\'m here to provide further assintance on how to use this bot.\nBut later, I\'m not in the mood right now')


def dog(bot, update):
    update.message.reply_text('This command will work in a future release')


def cat(bot, update):
    update.message.reply_text('This command will work in a future release')


def echo(bot, update):
    """Echo the user message."""
    text = update.message.text
    finalText = extract_info(text)

    update.message.reply_text('Your entered text contains:\n\n'+finalText)

"""Start the bot."""
# Create the EventHandler and pass it your bot's token.
updater = Updater(token)

# Get the dispatcher to register handlers
dp = updater.dispatcher

# on different commands - answer in Telegram
dp.add_handler(CommandHandler("start", start))

dp.add_handler(CommandHandler("help", help))

dp.add_handler(CommandHandler("dog", dog))

dp.add_handler(CommandHandler("cat", cat))

# on noncommand i.e message - echo the message on Telegram
dp.add_handler(MessageHandler(Filters.text, echo))

# Start the Bot
updater.start_polling()
updater.idle()