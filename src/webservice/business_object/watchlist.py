from src.webservice.business_object.utilisateur import Utilisateur


class Watchlist:
    def __init__(
        self, nom_watchlist: str, id_utilisateur, list_film=None, id_watchlist=None
    ):
        """Constructeur avec validation basique et initialisation des attributs.

        Parameters
        ----------
        nom_watchlist : str
            Nom de la watchlist.
        id_utilisateur : int
            Identifiant de l'utilisateur associé.
        list_film : list, optional
            Liste des films dans la watchlist. Si None, une liste vide sera initialisée.
        id_watchlist : int, optional
            Identifiant de la watchlist. Si None, un nouvel identifiant sera généré.
        """

        # Validation des types
        if not isinstance(nom_watchlist, str):
            raise TypeError(
                f"nom_watchlist doit être une chaîne de caractères, mais reçu {type(nom_watchlist).__name__}"
            )

        if not isinstance(id_utilisateur, int):
            raise TypeError(
                f"id_utilisateur doit être un entier, mais reçu {type(id_utilisateur).__name__}"
            )

        if list_film is not None and not isinstance(list_film, list):
            raise TypeError(
                f"list_film doit être une liste ou None, mais reçu {type(list_film).__name__}"
            )

        if id_watchlist is not None and not isinstance(id_watchlist, int):
            raise TypeError(
                f"id_watchlist doit être un entier ou None, mais reçu {type(id_watchlist).__name__}"
            )

        # Initialisation des attributs
        self.id_watchlist = id_watchlist
        self.nom_watchlist = nom_watchlist
        self.id_utilisateur = id_utilisateur
        self.list_film = list_film if list_film is not None else []

    def get_nom_watchlist(self):
        self.nom_watchlist

    def get_list_film(self):
        self.list_film

    def verifier_utilisateur(self, utilisateur: Utilisateur) -> bool:
        """
        Vérifie si l'utilisateur est une instance de Utilisateur et s'il s'agit
        du bon utilisateur.

        Paramètres :
        ------------
        utilisateur : Utilisateur
            L'utilisateur à vérifier.

        Returns :
        ---------
        bool
            True si l'utilisateur correspond, sinon False.

        Exceptions :
        ------------
        TypeError
            Si l'utilisateur n'est pas une instance de Utilisateur.
        """
        # Vérification du type de l'utilisateur
        if not isinstance(utilisateur, Utilisateur):
            raise TypeError(
                f"utilisateur doit être une instance de Utilisateur, mais reçu {type(utilisateur).__name__}"
            )

        # Vérifie si l'identifiant de l'utilisateur correspond
        return self.id_utilisateur == utilisateur.id_utilisateur
