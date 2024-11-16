from src.webservice.business_object.plateforme import PlateformeStreaming
from src.webservice.business_object.abonnement import Abonnement
from src.webservice.dao.abonnement_dao import AbonnementDao


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
        abonnement = Abonnement(id_abonnement, "ds")
        prix = AbonnementDao().get_prix_abonnement_DAO(abonnement)
        return prix

    def pub_abonnement(self, id_abonnement):
        """
        Vérifie si un abonnement spécifique contient des publicités.

        Attributs
        ----------
        id_abonnement : L'identifiant de l'abonnement pour lequel on souhaite vérifier la présence de publicités.

        Returns : 
        str : Une chaîne de caractères indiquant si l'abonnement contient ou non des publicités.
        """
        
        abonnement = Abonnement(id_abonnement, "ds")
        pub = AbonnementDao().get_pub_abonnement_DAO(abonnement)
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
        abonnement = Abonnement(id_abonnement, 'ds')
        qualite = AbonnementDao().get_qualite_abonnement_DAO(abonnement)
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
        abonnement_list = AbonnementDao().get_nom_abonnement_DAO(plateforme)
        return abonnement_list

    
