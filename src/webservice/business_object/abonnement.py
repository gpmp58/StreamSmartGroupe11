class Abonnemennt:
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

    def __init__(self, nom_abonnement: str, logo_plateforme: str, id_plateforme: str):
        """Constructeur avec validation basique"""
         """
        Initialise un objet PlateformeStreaming avec les attributs spécifiés.

        Args:
            nom_plateforme (str) : Le nom de la plateforme renseigné.
            logo_plateforme (str) : Le logo de la plateforme renseigné.
            id_plateforme (str) : L'id de la plateforme renseigné.

        Raises:
            Exception: Si le nom de la plateforme n'est pas une chaîne de caractères.
            Exception: Si le logo de la plateforme n'est pas une chaîne de caractères.
            Exception: Si l'identifiant de la plateforme n'est pas une chaîne de caractères.
        """

        if not isinstance(nom_plateforme, str):
            raise Exception("Le nom de la plateforme n'est pas une chaîne de caractères.")
        if not isinstance(logo_plateforme, str):
            raise Exception("Le logo de la plateforme n'est pas une chaîne de caractères.")
        if not isinstance(id_plateforme, str):
            raise Exception("L'identifiant de la plateforme n'est pas une chaîne de caractères.")

        self.id_plateforme = id_plateforme
        self.nom_plateforme = nom_plateforme
        self.logo_plateforme = logo_plateforme

    def info_plateforem(self) -> dict:
        """Retourne les attributs de la plateforme sous forme de dictionnaire"""
        return {
            "Nom_plateforme": self.nom_plateforme,
            "logo_plateforme": self.logo_plateforme,
            "id_plateforme": self.id_plateforme,
        }

    def get_nom_plateforme(self):
        return self.nom_plateforme

    def get_logo_plateforme(selft): 
        return self.logo_plateforme

    def get_id_plateforme(self):
        return self.id_plateforme    