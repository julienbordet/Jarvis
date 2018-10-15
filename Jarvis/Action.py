import logging
import json

import Crypto
from Jarvis.JEncoder import JEncoder

class Action:

    def __init__(self):
        pass

    def check_function(self):
        logging.info("Action class check_function")
        return None

    def save(self, f):
        """
        Méthode générique pour sauvegarde les attributs des objets sous forme JSON.
        Génère le JSON et l'écrit dans le fichier

        NB : Pour le moment, on ne gère qu'une seule instance par classe

        :param f:
        Objet fichier pour l'écriture

        :return:

        """

        logging.info("Dictionnaire : {0}".format(self.__dict__))

        s = json.dumps(self, cls=JEncoder)
        f.write(s + "\n")
