from src.webservice.business_object.plateforme import PlateformeStreaming
from src.webservice.business_object.abonnement import Abonnement
from src.dao.abonnement_dao import AbonnementDao


class AbonnementService():
    """
    Service de gestion des abonnements. Cette classe fournit des méthodes pour récupérer des informations sur les abonnements, y compris le prix, la présence de publicités, la qualité de l'abonnement, et pour effectuer une recherche d'abonnement en fonction de la plateforme de streaming.
    """

    def prix_abonnement(self, id_abonnement):
        """
        Récupère le prix d'un abonnement en fonction de son identifiant.

        Args:
            id_abonnement (int) : L'identifiant de l'abonnement pour lequel il faut récupérer le prix.

        Returns:
            float : Le prix de l'abonnement.
        """        
        abonnement = Abonnement(id_abonnement)
        prix = AbonnementDao().get_prix_DAO(abonnement)
        return prix

    def pub_abonnement(self, id_abonnement):
        abonnement = Abonnement(id_abonnement)
        pub = AbonnementDao().get_pub_DAO(abonnement)
        if pub :
            return f"Cet abonnement contient des pub !"
        else :
            return f"Cet abonnement ne contient pas des pub !"

    def qualite_abonnement(self, id_abonnement):
        """
        Récupère la qualité de l'abonnement.

        Args:
            id_abonnement (int) : L'ID de l'abonnement pour lequel il faut récupérer la qualité.

        Returns:
            str : La qualité de l'abonnement.
        """        
        abonnement = Abonnement(id_abonnement)
        qualite = AbonnementDao().get_qualite_DAO(abonnement)
        return qualite
    
    def recherche_abonnement(self, nom_plateforme, id_plateforme):
        """
        Recherche des abonnements disponibles pour une plateforme de streaming donnée.

        Args:
            nom_plateforme (str) : Le nom de la plateforme de streaming.
            id_plateforme (int) : L'identifiant de la plateforme de streaming.

        Returns:
            list : Une liste des abonnements disponibles pour la plateforme spécifiée.
        """        
        plateforme = PlateformeStreaming(nom_plateforme, id_plateforme)
        abonnement_list = AbonnementDao().get_abonnement(plateforme)
        return abonnement_list

    
