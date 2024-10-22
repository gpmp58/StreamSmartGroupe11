
from src.webservice.dao.db_connection import DBConnection

from src.webservice.business_object.abonnement import Abonnement

from src.webservice.business_object.plateforme import Plateforme


class AbonnementDao():
    """Classe contenant les méthodes pour recuperer les infos d'un abonnement"""

    def rechercher_prix_DAO(self,  abonnement: Abonnement) -> tuple:
        """Cette méthode recherche les infos sur un abonnement"""

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


    def rechercher_pub_DAO(self,  abonnement: Abonnement) -> tuple:
        """Cette méthode recherche les infos sur un abonnement"""
        
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
    
    
def rechercher_qualite_DAO(self,  abonnement: Abonnement) -> tuple:
        """Cette méthode recherche les infos sur un abonnement"""
        
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
    
def rechercher_abonnement(self, plateforme: Plateforme) -> list:
        """
        Cette méthode recherche les abonnements d'une plateforme"""
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
