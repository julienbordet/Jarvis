# -*- coding: utf-8 -*-

import re
import logging
import json
from threading import Thread
from time import sleep

from Jarvis.Crypto import Crypto
from Jarvis.JEncoder import JEncoder


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
        self.sleep_time = 300
        self.alert_handler = None
        self.dump_file = 'jarvis_dump.txt'
        self._conf = {}

        try:
            f = open(self.dump_file, 'r')
        except IOError:
            logging.warning("Récupérération du dump impossibe lors de l'ouverture du fichier {0}".format(
                self.dump_file))
            return

        for line in f:
            attribut = re.search(r"(.*?)#(.*)", line)
            self._conf[attribut.group(1)] = attribut.group(2)
            logging.info("Lecture du fichier dump : {0}".format(self._conf))

        json_dict = dict()

        json_key = "{0}.{1}".format(self.__class__.__module__, self.__class__.__qualname__)
        if json_key in self._conf.keys():
            json_string = self._conf[json_key]
            json_dict = json.loads(json_string)

            if "last_command" in json_dict.keys(): self.last_command = json_dict["last_command"]
            if "sleep_time" in json_dict.keys(): self.sleep_time = json_dict["sleep_time"]

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

        json_dict = dict()

        json_key = "{0}.{1}".format(Crypto.__module__, Crypto.__qualname__)
        if json_key in self._conf.keys():
            json_string = self._conf[json_key]
            json_dict = json.loads(json_string)

        crypto = Crypto(api, key, **json_dict)

        self.ACTIONS.append(crypto)
        for i in crypto.command_list():
            self.COMMAND_LIST[i] = crypto

    def send_command(self, data):
        """
        Gestion des commandes reçues de la part du gestionnaire d'interaction (Telegram, ligne de commande...)

        :param data:
        Chaîne de caractère représentant les données transmises de l'utilisateur

        :return:
        La réponse de l'objet action enregistré dans la table COMMAND_LIST

        """

        logging.info("In send_command : data = {0}".format(data))

        # Séparation de la commande et des paramètres, qui sont optionnels
        words = re.search(r"([\w\.]+)\s*(.*)", data)

        if not words:
            return u"Problème dans le traitement de la commande"

        self.last_command = data

        command = words.group(1).lower()
        params = words.group(2)

        logging.info("In send_command : command = {0}, params = {1}".format(command, params))

        if command == ".":
            command = self.last_command

        if command == "save":
            self.save()
            return "Save : sauvegarde effectuée"

        if command == "sleep" and params is not None:
            try:
                sleep_time = float(params)
            except Exception:
                return "Erreur : paramètre incorrect"

            self.sleep_time = sleep_time
            return "Sleep : modification effectuée"

        if not command in self.COMMAND_LIST.keys():
            return u"Désolé, commande inconnue"
        else:
            logging.info("Commande : " + command + " paramètres : " + params)
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
        """
        Lance le threading pour effectuer les surveillance définies par les objets stockés dans ACTIONS

        :return:

        """
        self._ready = True
        self.thread.start()

    def manage_checks(self):
        """
        Méthode lancée par le Thread principal. Fait le tour des objets de classe Action stockés dans ACTIONS
        et lance si disponible la méthode check_function()

        La méthode check_function renvoie un message à afficher à l'utilisateur. Cette chaîne est alors passée
        comme paramètre à la méthode handler, qui a été configurée plus tôt.

        :return:

        """
        if self._ready == False:
            return

        while (1):
            logging.info("manage_check called (self._ready = {0})".format(self._ready))
            i = 1
            for action in self.ACTIONS:
                logging.info("Review actions {0}".format(i))
                msg = action.check_function()

                if (msg is not None):
                    logging.info(" Msg is not None : " + msg)

                    if self.alert_handler is not None:
                        self.alert_handler(msg)
                else:
                    logging.info(" Msg is None")

            sleep(self.sleep_time)

    def jsonable(self):
        """
            Méthode appelée par le classe JEncoder pour permettre à chaque sous-classe de Action de définir ses propres
            attributs à sauvegarder.
            L'objectif principal est d'éviter de sérialiser les attributs complexes du type Coinbase

            :param o:
            L'objet à sérialiser

            :return:
            Le dictionnaire prêt à sérialiser


            """

        return {'last_command' : self.last_command, 'sleep_time' : self.sleep_time}

    def save(self):
        """
        Ouvre un fichier, puis le passe à chacun des objets stockés dans ACTION pour qu'il puisse y stocker ses
        informations au format JSON

        :return:

        """

        try:
            f = open(self.dump_file, 'w')
        except IOError:
            logging.warning("Dump impossible : erreur lors de l'ouverture du fichier {0}".format(self.dump_file))
            return

        f.write("{0}.{1}#".format(self.__class__.__module__, self.__class__.__qualname__))
        s = json.dumps(self, cls=JEncoder)
        f.write(s + "\n")

        for action in self.ACTIONS:
            f.write("{0}.{1}#".format(action.__class__.__module__, action.__class__.__qualname__))
            action.save(f)

