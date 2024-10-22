from sevice_abonnement import AbonnementService

from abonnement_dao import AbonnementDao

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

    def __init__(self, id_abonnement: int):
        """Constructeur avec validation basique"""
        """
        Initialise un objet Abonnement avec les attributs spécifiés.

        Args:
            nom_abonnement (str) : Le nom de l'abonnement renseigné.
            id_abonnement (str) : L'id de l'abonnement renseigné.

        Raises:
            Exception: Si le nom de l'abonnement n'est pas une chaîne de caractères.
            Exception: Si l'identifiant de l'abonnement n'est pas un entier.
        """

        if not isinstance(id_abonnement, int):
            raise Exception(
                "L'identifiant de l'abonnement n'est pas un entier.")

        self.id_abonnement = id_abonnement
        self.qualite = self.qualite_abonnement()
        self.prix = self.prix_abonnement()
        self.pub = self.pub_abonnement()
        self.nom_abonnement = self.rechercher_nom_abonnement_DAO()

    def info_abonnement(self) -> dict:
        """Retourne les attributs de l'abonnement sous forme de dictionnaire"""
        return {
            "Nom_abonnement": self.nom_abonnement,
            "prix": self.prix,
            "id_abonnement": self.id_abonnement,
            "pub": self.pub,
            "qualité": self.qualite,
        }

    def get_nom_abonnement(self):
        return self.nom_abonnement

    def get_prix(self):
        return self.prix

    def get_id_abonnement(self):
        return self.id_abonnement

    def get_qualite(self):
        return self.qualite

    def get_pub(self):
        return self.pub
