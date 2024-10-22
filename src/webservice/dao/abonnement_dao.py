
from src.webservice.dao.db_connection import DBConnection

from src.webservice.business_object.abonnement import Abonnement

from src.webservice.business_object.plateforme import Plateforme


class AbonnementDao():
    """Classe contenant les méthodes pour recuperer les infos d'un abonnement"""

    def rechercher_prix__abonnement_DAO(self,  abonnement: Abonnement) -> tuple:
        """Cette méthode renvoie le prix d'un abonnement"""

        prix = None
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT prix FROM abonnement             "
                    " WHERE id_abonnement = %(id_abonnement)s      ",
                    {"id_abonnement": abonnement.id_abonnement},
                )
                prix = cursor.fetchone()

        return prix


    def rechercher_pub__abonnement_DAO(self,  abonnement: Abonnement) -> tuple:
        """Cette méthode renvoie true si l'abonnement fait de la pub"""
        
        pub = None
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT pub FROM abonnement             "
                    " WHERE id_abonnement = %(id_abonnement)s      ",
                    {"id_abonnement": abonnement.id_abonnement},
                )
                pub = cursor.fetchone()

        return pub
    
    
    def rechercher_qualite_abonnement_DAO(self,  abonnement: Abonnement) -> tuple:
        """Cette méthode recherche la qualité d'un abonnement"""
        
        qualite = None
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT qualite FROM abonnement             "
                    " WHERE id_abonnement = %(id_abonnement)s      ",
                    {"id_abonnement": abonnement.id_abonnement},
                )
                qualite = cursor.fetchone()

        return qualite
   
   
    def rechercher_nom_abonnement_DAO(self,  abonnement: Abonnement) -> tuple:
        """Cette méthode recherche le nom d'un abonnement"""
        
        nom = None
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT nom_abonnement FROM abonnement             "
                    " WHERE id_abonnement = %(id_abonnement)s      ",
                    {"id_abonnement": abonnement.id_abonnement},
                )
                nom = cursor.fetchone()

        return nom
   
    
    def rechercher_abonnement_par_plateforme_DAO(self, plateforme: Plateforme) -> list:
        """Cette méthode fournit la liste d'abonnements d'une plateforme"""
        abonnements = []
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id_abonnement   "
                    "FROM utilisateur           "
                    "WHERE nom_plateforme = %(nom_plateforme)s",
                    {"nom_plateforme": abonnement.nom_plateforme},
                )
                abonnements = fetchall()

        return abonnements
