
class Critere():
    """
    Classe représentant un critère de filtrage appliqué à une watchlist.

    Attributs
    ---------
    watchlist : Watchlist
        L'instance de la classe Watchlist qui est associée à ces critères de filtrage.
    
    criteres : dict
        Un dictionnaire contenant les critères de filtrage. Chaque clé correspond à un critère et la valeur associée est du type attendu selon ce critère.

    """


    def __init__(self, id_watchlist, criteres):

        if not isinstance(id_watchlist, int):
            raise Exception(
                "L'id watchlist n'est pas un entier.")
        if not isinstance(criteres, dict):
            raise Exception(
                "criteres n'est pas un dictionnaire.")
          
        types_attendus = [str, bool, bool, bool]

        for valeur, (key, types_attendus) in enumerate(zip(criteres.values(), types_attendus)):
            assert isinstance(criteres[key], types_attendus), f"La valeur de la clé {key} n'est pas du type {types_attendus.__name__}."        

        self.id_watchlist = id_watchlist
        self.criteres = criteres

    def get_id_watchlist(self):
        return self.id_watchlist
    def get_critere(self):
        """
        Retourne le dictionnaire des critères associés à la watchlist.

        Retour
        ------
        dict
            Le dictionnaire des critères de filtrage associés à cette watchlist.
        """        
        return self.criteres