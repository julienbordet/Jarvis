"""
    Implémentation de la classe Crypto, qui utilise Coinbase pour récupérer des informations sur les cours
"""

from Jarvis.Action import Action
import logging
import json
from coinbase.wallet.client import Client
import re

class Crypto(Action):
    COMMAND_LIST = ['btc']

    def __init__(self, api_key, api_secret):
        super().__init__()

        cb_api_key = api_key
        cb_api_secret = api_secret

        self.cb_client =  Client(cb_api_key, cb_api_secret)

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

            price = self.cb_client.get_spot_price(currency_pair = 'BTC-' + currency)
            return u"1 bitcoin = " + price.amount + " " + currency

        return u"Houra"

    def check_function(self):
        price = float(self.cb_client.get_spot_price(currency_pair = 'BTC-EUR').amount)
        if price > 5680:
            return "Hey, dites, la valeur semble intéressante"
        else:
            return "Bof rien à dire sur la valeur"
