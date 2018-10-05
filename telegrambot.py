#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Jarvis.Input import Input
import re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import pprint
import configparser

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

def start(bot, update):
    update.message.reply_text("Hi all")

def manageDialog(bot, update):
    logger.info("In manageDialog")
    update.message.reply_text(j.send_command(update.message.text))

def main():
    global j

    # La configuration est lue dans le fichier config.ini présent dans le même répertoire que le script
    config = configparser.ConfigParser()
    config.read('config.ini')

    cb_api_key = config['COINBASE']['KEY']
    cb_api_secret = config['COINBASE']['SECRET']
    token = config['TELEGRAM']['TOKEN']

    j = Input()

    j.register_crypto(cb_api_key, cb_api_secret)

    """
    Démarrage du bot
    """

    updater = Updater(token)
                   
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text,manageDialog))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
