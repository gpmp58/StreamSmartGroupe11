class Abonnement:
    """
    Classe représentant un abonnement sur une plateforme de streaming

    Attributs
    ----------
    id_abonnement : int
        identifiant
    nom_abonnement : str
        nom de l'abonnement
    prix : int or float
        prix de l'abonnement
    detail_offre : str
        détail de l'offre proposée par l'abonnement
    """

    def __init__(
        self, nom_abonnement: str, prix: float, id_abonnement: int, detail_offre: str
    ):
        """Constructeur avec validation basique"""
        """
        Initialise un objet Abonnement avec les attributs spécifiés.

        Args:
            nom_abonnement (str) : Le nom de l'abonnement renseigné.
            prix (float) : Le prix de l'abonnement renseigné.
            id_abonnement (str) : L'id de l'abonnement renseigné.
            detail_offre (str) : Le détail de l'offre renseigné.

        Raises:
            Exception: Si le nom de l'abonnement n'est pas une chaîne de caractères.
            Exception: Si le prix de l'abonnement n'est pas un flottant.
            Exception: Si l'identifiant de l'abonnement n'est pas une chaîne de caractères.
            Exception: Si le detail de l'offre n'est pas une chaîne de caractères.
        """

        if not isinstance(nom_abonnement, str):
            raise Exception(
                "Le nom de l'abonnement n'est pas une chaîne de caractères."
            )
        if not isinstance(prix, float):
            raise Exception("Le prix de l'abonnement n'est pas un flottant.")
        if not isinstance(id_abonnement, int):
            raise Exception(
                "L'identifiant de l'abonnement n'est pas une chaîne de caractères."
            )
        if not isinstance(detail_offre, str):
            raise Exception("Le detail de l'offre n'est pas une chaîne de caractères.")

        self.id_abonnement = id_abonnement
        self.nom_abonnement = nom_abonnement
        self.prix = prix
        self.detail_offre = detail_offre

    def info_abonnement(self) -> dict:
        """Retourne les attributs de l'abonnement sous forme de dictionnaire"""
        return {
            "Nom_abonnement": self.nom_abonnement,
            "prix": self.prix,
            "id_abonnement": self.id_abonnement,
            "detail_offre": self.detail_offre,
        }

    def get_nom_abonnement(self):
        return self.nom_abonnement

    def get_prix(self):
        return self.prix

    def get_id_abonnement(self):
        return self.id_abonnement

    def get_detail_offre(self):
        return self.detail_offre
