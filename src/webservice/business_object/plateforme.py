class PlateformeStreaming:
    """
    Classe représentant une Plateforme de streaming.

    Attributs
    ----------
    id_plateforme : int
        identifiant
    nom_plateforme : str
        nom de la plateforme
    logo_plateforme : str
        logo de la plateforme
    """

    def __init__(self, nom_plateforme: str, id_plateforme: int, logo_plateforme = None):                                
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
            raise Exception(
                "Le nom de la plateforme n'est pas une chaîne de caractères."
            )
        if not isinstance(logo_plateforme, str) and logo_plateforme is not None :
            raise Exception(
                "Le logo de la plateforme n'est pas une chaîne de caractères ou n'est pas égal à None."
            )
        if not isinstance(id_plateforme, int):
            raise Exception("L'identifiant de la plateforme n'est pas un entier.")

        self.id_plateforme = id_plateforme
        self.nom_plateforme = nom_plateforme
        self.logo_plateforme = logo_plateforme

    def info_plateforme(self) -> dict:
        """
        Retourne les attributs de la plateforme sous forme de dictionnaire
        
        Returns:
            dict : Attributs de la plateforme.
        """
        return {
            "Nom_plateforme": self.nom_plateforme,
            "logo_plateforme": self.logo_plateforme,
            "id_plateforme": self.id_plateforme,
        }

    def get_nom_plateforme(self):
        """
        Retourne le nom de la plateforme de streaming.

        Returns:
            str : Nom de la plateforme.
        """         
        return self.nom_plateforme

    def get_logo_plateforme(self):
        """
        Retourne le logo de la plateforme de streaming.

        Returns:
            str : Logo de la plateforme.
        """         
        return self.logo_plateforme

    def get_id_plateforme(self):
        """
        Retourne l'identifiant de la plateforme de streaming. 

        Returns:
            int : Identifiant de la plateforme.
        """         
        return self.id_plateforme
