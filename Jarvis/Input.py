# -*- coding: utf-8 -*-

import re
from Jarvis.Crypto import Crypto

class Input:
    """
        La table de hash COMMAND_LIST contient l'ensemble des commandes autorisées
        La valeur de chaque entrée est l'objet en charge de la gestion de la commande
        Cette liste est complétée lors du lancement de __init__
    """
    COMMAND_LIST = {}
    CHECK_FUNCTIONS = {}

    def __init__(self):
        pass

    def register_crypto(self, api, key):
        # Enregistrement du type d'objet Crypto.
        crypto = Crypto(api, key)
        for i in crypto.command_list():
            self.COMMAND_LIST[i] = crypto

        fcheck = crypto.check_function()
        if fcheck != None:
            self.CHECK_FUNCTIONS.append(fcheck)


    """
        Gestion des commandes reçues de la part du gestionnaire d'interaction (Telegram, ligne de commande...)
    """
    def send_command(self, data):
        print("On me parle : ", data)

        # Séparation de la commande et des paramètres, qui sont optionnels
        words = re.search(r"(\w+)\s*(.*)", data)

        if not words:
            return u"Problème dans le traitement de la commande"

        command = words.group(1).lower()
        params = words.group(2)

        if not command in self.COMMAND_LIST.keys():
            return u"Désolé, commande inconnue"
        else:
            print( "Commande : " + command + " paramètres : " + params)
            manager = self.COMMAND_LIST[command]
            return manager.get_response(command, params)
