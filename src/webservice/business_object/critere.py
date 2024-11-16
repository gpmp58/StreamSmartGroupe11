from src.webservice.business_object.watchlist import Watchlist

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


    def __init__(self, watchlist, criteres):
        """
        Initialise un objet Critere avec une watchlist et un dictionnaire de critères.

        Args : 
           watchlist (Watchlist) : L'instance de la classe `Watchlist` qui sera associée aux critères.
           criteres (dict) : Un dictionnaire contenant les critères à appliquer à la watchlist. 

        Raises :
            Exception: Si watchlist n'est pas une instance de Watchlist.
            Exception: Si criteres n'est pas un dictionnaire. 
            Exception: Si un des critères n'est pas du type attendu.
        """
        if not isinstance(watchlist, Watchlist):
            raise Exception(
                "La watchlist n'est pas une instance Watchlist.")
        if not isinstance(criteres, dict):
            raise Exception(
                "criteres n'est pas un dictionnaire.")
          
        types_attendus = [str, bool, bool, bool]

        for valeur, (key, types_attendus) in enumerate(zip(criteres.values(), types_attendus)):
            assert isinstance(criteres[key], types_attendus), f"La valeur de la clé {key} n'est pas du type {types_attendus.__name__}."        

        self.watchlist = watchlist
        self.criteres = criteres

    def get_watchlist(self):
        """
        Retourne l'instance de la watchlist associée à cet objet Critere.

        Retour
        ------
        Watchlist
            L'instance de la Watchlist associée à cet objet Critere.
        """        
        return self.watchlist

    def get_critere(self):
        """
        Retourne le dictionnaire des critères associés à la watchlist.

        Retour
        ------
        dict
            Le dictionnaire des critères de filtrage associés à cette watchlist.
        """        
        return self.criteres