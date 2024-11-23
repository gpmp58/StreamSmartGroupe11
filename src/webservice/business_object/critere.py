class Critere:
    """
    Classe représentant un critère de filtrage appliqué à une watchlist.

    Attributs
    ---------
    id_watchlist : int

    criteres : dict
        Un dictionnaire contenant les critères de filtrage.
        Chaque clé correspond à un critère : prix , qualite ,
        pub et rapport_quantite_prix
        la valeur associée est du type attendu selon ce critère.

    """

    def __init__(self, id_watchlist, criteres):
        "Initialisation de la classe"
        if not isinstance(id_watchlist, int):
            raise Exception("L'id watchlist n'est pas un entier.")
        if not isinstance(criteres, dict):
            raise Exception("criteres n'est pas un dictionnaire.")

        types_attendus = {
            "qualite": str,
            "pub": bool,
            "prix": bool,
            "rapport_quantite_prix": bool,
        }

        for key, valeur in criteres.items():
            if key not in types_attendus:
                raise Exception(
                    f"Clé {key} inconnue dans les critères."
                )
            expected_type = types_attendus[key]
            if not isinstance(valeur, expected_type):
                raise Exception(
                    f"La valeur de la clé {key} n'est pas"
                    f" du type {expected_type.__name__}."
                )

        self.id_watchlist = id_watchlist
        self.criteres = criteres

    def get_id_watchlist(self):
        """
        Retourne l'id_watchlist.

        Return
        ------
        int
        """
        return self.id_watchlist

    def get_critere(self):
        """
        Retourne le dictionnaire des critères associés à la watchlist.

        Return
        ------
        dict
            Le dictionnaire des critères de filtrage
            associés à cette watchlist.
            clés de dict : prix,qualite,pub,rapport_quantite_prix
        """
        return self.criteres
