"""
    Implémentation de la classe Crypto, qui utilise Coinbase pour récupérer des informations sur les cours
"""

from coinbase.wallet.client import Client

from Jarvis.Action import Action


class Crypto(Action):
    COMMAND_LIST = ['btc', 'low', 'high']

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

    def __init__(self, api_key, api_secret):
        """

        Constructeur de la classe Crypto

        Appelle le constructeur de la classe mère, créé l'objet client Coinbase et initialise les attributs de base

        """

        super().__init__()

        cb_api_key = api_key
        cb_api_secret = api_secret

        self.cb_client = Client(cb_api_key, cb_api_secret)

        self.low_threshold = None
        self.high_threshold = None

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

        if command == 'btc':
            currency = 'EUR'

            if params.lower() == 'usd':
                currency = 'USD'

            price = self.cb_client.get_spot_price(currency_pair='BTC-' + currency)
            return u"1 bitcoin = " + price.amount + " " + currency

        if command == 'low':
            low = float(params.lower())
            self.set_low_threshold(low)
            return u"Alerte inférieure configurée désormais à {0}".format(low)

        if command == 'high':
            high = float(params.lower())
            self.set_high_threshold(high)
            return u"Alerte supérieure configurée désormais à {0}".format(high)

        return u"Hou là, ce n'est pas bon signe..."

    def check_function(self):
        """

        Effectue un certain nombre de vérification et lance l'alerte associée

        :return:

        """

        price = float(self.cb_client.get_spot_price(currency_pair='BTC-EUR').amount)

        if self.low_threshold is not None and price < self.low_threshold:
            return u"Le prix " + price + " est inférieur à la valeur minimale"
        elif self.high_threshold is not None and price > self.high_threshold:
            return u"Le prix " + price + " est supérieur à la valeur minimale"
