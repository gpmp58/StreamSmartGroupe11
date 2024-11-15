
class Critere():

    def __init__(self, id_watchlist, criteres):

        if not isinstance(id_watchlist, int):
            raise Exception(
                "L'id watchlist n'est pas un entier.")
        if not isinstance(criteres, dict):
            raise Exception(
                "critere n'est pas un dictionnaire.")

        self.id_watchlist = id_watchlist
        self.criteres = criteres

    def get_id_watchlist(self):
        return self.id_watchlist
    def get_critere(self):
        return self.criteres