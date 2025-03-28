from src.webservice.business_object.utilisateur import Utilisateur


class Watchlist:
    def __init__(
        self,
        nom_watchlist: str,
        id_utilisateur,
        list_film=[],
        id_watchlist: int = None,
    ):
        """
        Classe représentant une watchlist.

        Attributs
        ----------
        nom_watchlist : str
            Nom de la watchlist.
        id_utilisateur : int
            Identifiant de l'utilisateur associé.
        list_film : list
            Liste des films dans la watchlist.
            Si None, une liste vide sera initialisée.
        id_watchlist : int, optional
            Identifiant de la watchlist.
            Si None, un nouvel identifiant sera généré.
        """
        if not isinstance(nom_watchlist, str):
            raise TypeError(
                f"nom_watchlist doit être une chaîne de caractères,"
                f" mais reçu {type(nom_watchlist).__name__}"
            )

        if not isinstance(id_utilisateur, int):
            raise TypeError(
                f"id_utilisateur doit être un entier,"
                f" mais reçu {type(id_utilisateur).__name__}"
            )

        if not isinstance(list_film, list):
            raise TypeError(
                f"list_film doit être une liste ou None,"
                f" mais reçu {type(list_film).__name__}"
            )

        if (
            not isinstance(id_watchlist, int)
            and id_watchlist is not None
        ):
            raise TypeError(
                f"id_watchlist doit être un entier ou None,"
                f" mais reçu {type(id_watchlist).__name__}"
            )

        # Initialisation des attributs
        self.id_watchlist = id_watchlist
        self.nom_watchlist = nom_watchlist
        self.id_utilisateur = id_utilisateur
        self.list_film = list_film

    def get_nom_watchlist(self):
        """
        Retourne le nom de la watchlist.

        Returns:
            str : Nom de la watchlist.
        """
        return self.nom_watchlist

    def get_list_film(self):
        """
        Retourne la liste des films dans la watchlist.

        Returns:
            list : Films de la watchlist.
        """
        return self.list_film

    def verifier_utilisateur(self, utilisateur: Utilisateur) -> bool:
        """
        Vérifie si l'utilisateur est une instance
        de Utilisateur et si c'est le bon utilisateur.

        Arguments
        ----------
        utilisateur : Utilisateur
            L'utilisateur à vérifier.

        Returns
        -------
        bool
            True si l'utilisateur correspond, sinon False.

        Raises
        ------
        TypeError
            Si l'utilisateur n'est pas une instance de Utilisateur.
        """
        if not isinstance(utilisateur, Utilisateur):
            raise TypeError(
                "utilisateur doit être une instance de Utilisateur"
            )

        return self.id_utilisateur == utilisateur.id_utilisateur
