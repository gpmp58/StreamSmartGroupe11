from src.webservice.business_object.watchlist import Watchlist

class Critere():

    def __init__(self, watchlist, criteres):

        if not isinstance(watchlist, Watchlist):
            raise Exception(
                "La watchlist n'est pas une instance Watchlist.")
        if not isinstance(criteres, dict):
            raise Exception(
                "critere n'est pas un dictionnaire.")

        self.watchlist = watchlist
        self.criteres = criteres

    def get_watchlist(self):
        return self.watchlist
    def get_critere(self):
        return self.criteres