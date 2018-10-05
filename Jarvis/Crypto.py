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

    """
        Fonctions d'échange avec l'utilisateur
    """

    def get_response(self, command, params):
        if command == 'btc':
            currency = 'EUR'

            if params.lower() == 'usd':
                currency = 'USD'

            price = self.cb_client.get_spot_price(currency_pair = 'BTC-' + currency)
            return u"1 bitcoin = " + price.amount + " " + currency

        return u"Houra"
