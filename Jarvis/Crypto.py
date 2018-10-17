"""
    Implémentation de la classe Crypto, qui utilise Coinbase pour récupérer des informations sur les cours
"""

from coinbase.wallet.client import Client
import logging

from Jarvis.Action import Action


class Crypto(Action):
    COMMAND_LIST = ['btc', 'zrx', 'low', 'high', 'cur']

    cb_api_key = None
    """ Clé pour l'API COINBASE """

    cb_api_secret = None
    """ Mot de passe pour l'API COINBASE"""

    cb_client = None
    """ Objet Coinbase pour gérer la connexion au site"""

    low_threshold = None
    """ Limite inférieure pour l'alerte"""

    high_threshold = None
    """ Limite supérieure pour l'alerte"""

    def __init__(self, api_key, api_secret, low_threshold=None, high_threshold=None, currency='EUR'):
        """

        Constructeur de la classe Crypto

        Appelle le constructeur de la classe mère, créé l'objet client Coinbase et initialise les attributs de base

        """
        super().__init__()

        cb_api_key = api_key
        cb_api_secret = api_secret

        self.cb_client = Client(cb_api_key, cb_api_secret)

        self.low_threshold = low_threshold
        self.high_threshold = high_threshold
        self.currency = currency

    def set_low_threshold(self, low_threshold):
        """

        Change la valeur minimale de l'alerte

        :param low_threshold:
        Nouvelle valeur minimale

        :return:

        """
        self.low_threshold = low_threshold

    def set_high_threshold(self, high_threshold):
        """

        Change la valeur maximale de l'alerte

        :param high_threshold:
        Nouvelle valeur maximale

        :return:

        """

        self.high_threshold = high_threshold

    def command_list(self):
        return self.COMMAND_LIST

    def get_response(self, command, params):
        """
            Fonction d'échange avec l'utilisateur

            :param command:
            La commande à exécuter

            :param params:
            Les paramètres propres à la commande

            :return:
            Le message à afficher en réponse à la commande, ou un message d'erreur

        """

        if command == 'btc' or command == 'zrx':
            price = self.cb_client.get_spot_price(currency_pair=command.capitalize() +'-' + self.currency)
            return u"1 bitcoin = " + price.amount + " " + self.currency

        if command == 'low':
            if not params:
                return "Plancher : {0}".format(self.low_threshold)

            try:
                low = float(params.lower())
            except ValueError:
                return "Paramètre incorrect"

            self.set_low_threshold(low)
            return u"Alerte plancher configurée désormais à {0}".format(low)

        if command == 'high':
            if not params:
                return "Plafond : {0}".format(self.high_threshold)

            try:
                high = float(params.lower())
            except ValueError:
                return "Paramètre incorrect"

            self.set_high_threshold(high)
            return u"Alerte plafond configurée désormais à {0}".format(high)

        if command == 'cur':
            if not params:
                return "Monnaie : {0}".format(self.currency)

            if params.lower() == 'usd':
                self.currency = 'USD'
                return "Modification effectuée"
            if params.lower() == 'eur':
                self.currency = 'EUR'
                return "Modification effectuée"

            return "Erreur sur la monnaie"

        return u"Hou là, ce n'est pas bon signe..."

    def check_function(self):
        """

        Effectue un certain nombre de vérification et lance l'alerte associée

        :return:
        Le message à afficher à l'utilisateur

        """
        logging.info("check_function")

        price = float(self.cb_client.get_spot_price(currency_pair='BTC-EUR').amount)
        logging.info("price is {0}".format(price))

        if self.low_threshold is not None and price < self.low_threshold:
            return u"Le prix {0} est inférieur au plancher".format(price)
        elif self.high_threshold is not None and price > self.high_threshold:
            return u"Le prix {0} est supérieur au plafond".format(price)

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

        new_dict = self.__dict__.copy()
        del new_dict["cb_client"]
        return new_dict

