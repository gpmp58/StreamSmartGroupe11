from src.webservice.dao.abonnement_dao import AbonnementDao
class Abonnement:
    """
    Classe représentant un abonnement.

    Attributs
    ----------
    id_abonnement : int
        identifiant
    nom_abonnement : str
        nom de l'abonnement
    prix : float
        prix de l'abonnement
    pub : bool
        pub de l'abonnement 
    qualité : str 
        qualité de l'abonnement 
    """

    def __init__(self, id_abonnement: int, nom_plateforme):
        """
        Initialise un objet Abonnement avec les attributs spécifiés.

        Args:
            nom_plateforme (str) : Le nom de l'abonnement renseigné.
            id_abonnement (int) : L'id de l'abonnement renseigné.

        Raises:
            Exception: Si le nom de la plateforme n'est pas une chaîne de caractères.
            Exception: Si l'identifiant de l'abonnement n'est pas un entier.
        """

        if not isinstance(id_abonnement, int):
            raise Exception(
                "L'identifiant de l'abonnement n'est pas un entier.")
        if not isinstance(nom_plateforme, str):
            raise Exception(
                "Le nom de la plateforme n'est pas une chaîne de caractère.")

        self.id_abonnement = id_abonnement
        self.nom_plateforme = nom_plateforme
        self.qualite = AbonnementDao().get_qualite_abonnement_DAO(id_abonnement)
        self.prix = AbonnementDao().get_prix_abonnement_DAO(id_abonnement)
        self.pub = AbonnementDao().get_pub_abonnement_DAO(id_abonnement)
        self.nom_abonnement = AbonnementDao().get_nom_abonnement_DAO(id_abonnement)

    def info_abonnement(self) -> dict:
        """
        Retourne les attributs de l'abonnement sous forme de dictionnaire
        
        Returns:
            dict : Attributs de l'abonnement.
        """
        return {
            "Nom_abonnement": self.nom_abonnement,
            "prix": self.prix,
            "id_abonnement": self.id_abonnement,
            "pub": self.pub,
            "qualité": self.qualite,
        }

    def get_nom_abonnement(self):
        """
        Retourne le nom de l'abonnement.

        Returns:
            str : Le nom de l'abonnement.
        """
        return self.nom_abonnement

    def get_prix(self):
        """
        Retourne le prix de l'abonnement.

        Returns:
            float : Le prix de l'abonnement.
        """        
        return self.prix

    def get_id_abonnement(self):
        """
        Retourne l'identifiant de l'abonnement.

        Returns:
            int : L'identifiant de l'abonnement.
        """        
        return self.id_abonnement

    def get_qualite(self):
        """
        Retourne la qualité, ie la résolution d'ecran proposée par l'abonnement.

        Returns:
            str : Qualité de l'abonnement.
        """        
        return self.qualite

    def get_pub(self):
        """
        Retourne l'agurment pub de l'abonnement, ie si l'abonnement diffuse des pubs ou non.

        Returns:
            bool : Pub de l'abonnement.
        """            
        return self.pub

if __name__ == "__main__":
    abonnement_test = Abonnement(1,"Canal+")
    information = abonnement_test.info_abonnement()
    print(abonnement_test.nom_plateforme)
