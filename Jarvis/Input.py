# -*- coding: utf-8 -*-

import re
from threading import Thread
from time import sleep

from Jarvis.Crypto import Crypto


class Input:
    """
    La classe Input est en charge la gestion de l'interface utilisateur

    Elle permet de gérer l'interface entre l'utilisateur qui interagit avec le bot (Telegram, ligne de commande)
    et les actions qui sont des instances de la classe Action et de ses classes dérivées

    Les méthodes register_ permet d'enregistrer les Actions au sein de l'objet Input, pour être utilisées plus tard
    La méthode send_command passe les commandes de l'utilisateur à l'objet approprié

    """

    # La table de hash COMMAND_LIST contient l'ensemble des commandes autorisées
    # La valeur de chaque entrée est l'objet en charge de la gestion de la commande
    # Cette liste est complétée lors du lancement du constructeur

    COMMAND_LIST = {}
    ACTIONS = []

    def __init__(self):
        """

        Constructeur de la classe input

        Pour le moment, on gère un thread unique, qui sera en charge d'exécuter la méthode manage_checks. Cette fonction
        est chargée d'appeler périodiquement les méthodes check_function des objets Actions gérés.

        """
        self._ready = False

        self.thread = Thread(target=self.manage_checks)

        self.last_command = ''

    def register_crypto(self, api, key):
        """
        Enregistrement du type d'objet Crypto

        :param api:
        Clé api pour Coinbase

        :param key:
        Chaîne key pour Coinbase

        :return:
        Rien

        """

        crypto = Crypto(api, key)

        self.ACTIONS.append(crypto)
        for i in crypto.command_list():
            self.COMMAND_LIST[i] = crypto

    def send_command(self, data):
        """
        Gestion des commandes reçues de la part du gestionnaire d'interaction (Telegram, ligne de commande...)

        :param data:
        Chaîne de caractère représentant les données transmises de l'utilisateur

        :return:
        La réponse de l'objet action enregistré la table COMMAND_LIST

        """

        print("On me parle : ", data)

        if data == '.':
            data = self.last_command

        # Séparation de la commande et des paramètres, qui sont optionnels
        words = re.search(r"(\w+)\s*(.*)", data)

        if not words:
            return u"Problème dans le traitement de la commande"

        command = words.group(1).lower()
        params = words.group(2)

        if not command in self.COMMAND_LIST.keys():
            return u"Désolé, commande inconnue"
        else:
            print("Commande : " + command + " paramètres : " + params)
            manager = self.COMMAND_LIST[command]
            return manager.get_response(command, params)

    def define_alert_handler(self, handler):
        """
        Définit la fonction en charge de propager l'alerte ou le message reçu

        :param handler:
        Fonction à appeler, en passant en paramètre la chaîne de caractère à envoyer

        """

        self.alert_handler = handler

    def start_polling(self):
        self._ready = True
        self.thread.start()

    def manage_checks(self):
        print("manage_check called (self._ready = {0})".format(self._ready))
        if self._ready == False:
            return

        while (1):
            i = 1
            for action in self.ACTIONS:
                print("Review actions {0}".format(i))
                msg = action.check_function()

                if (msg is not None):
                    print(" Msg is not None : " + msg)
                    self.alert_handler(msg)

            sleep(10)
