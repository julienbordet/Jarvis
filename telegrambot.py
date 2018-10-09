#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import logging
from time import sleep

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from Jarvis.Input import Input


def error(bot, update, error):
    logging.warning('Update "%s" caused error "%s"', update, error)


def save_chat_id(update):
    global chat_id

    # On sauvegarde chat_id si cela n'avait pas été fait auparavant
    if chat_id == None:
        chat_id = update.message.chat_id


def start(bot, update):
    """
    Gestion de la commande /start

    :type update: object

    """

    logging.info("In 'start' function")

    save_chat_id(update)
    update.message.reply_text("Hi all")


def manage_dialog(bot, update):
    """
    Handler des messages envoyés par l'utilisateur sur Telegram

    Sauvegarde si nécessaire le chat_id pour réutilisation plus tard

    """

    logging.info("In 'manage_dialog' function : " + update.message.text)

    save_chat_id(update)
    update.message.reply_text(j.send_command(update.message.text))


def handle_new_alert(msg):
    """
    Fonction appelée pour transmettre les informations à l'utilisateur
    
    Fonction "callback" appelée par le gestionnaire Input pour transmettre les informations 
    auprès de l'utilisateur

    :param msg:
    Message à renvoyer à l'utilisateur

    """

    global chat_id

    if chat_id == None:
        logging.warning("Tentative d'appel de handle_new_alert sans chat id")
        return

    logging.info("In 'handle_new_alert : " + msg)

    bot = updater.bot
    bot.sendMessage(chat_id=chat_id, text=msg)


def main():
    global j
    global chat_id
    global telegram_token
    global updater

    chat_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    logging.info("Démarrage de  " + __name__)

    #
    # La configuration est lue dans le fichier config.ini présent dans le même répertoire que le script
    #
    config = configparser.ConfigParser()
    config.read('config.ini')

    cb_api_key = config['COINBASE']['KEY']
    cb_api_secret = config['COINBASE']['SECRET']
    telegram_token = config['TELEGRAM']['TOKEN']

    j = Input()

    j.register_crypto(cb_api_key, cb_api_secret)
    # j.define_alert_handler(handle_new_alert)
    # j.start_polling()

    #
    # Démarrage du bot
    #

    updater = Updater(telegram_token)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, manage_dialog))
    dp.add_error_handler(error)
    updater.start_polling()

    #
    # Boucle infinie pour gérer les événements :
    #   1/ réception de messages de la part de l'utilisateur d'une part
    #   2/ alertes gérées par l'objet input d'autre part.
    #

    while (1):
        sleep(1)


if __name__ == '__main__':
    main()
