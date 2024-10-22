
from src.webservice.dao.db_connection import DBConnection

from src.webservice.business_object.abonnement import Abonnement


class AbonnementDao():
    """Classe contenant les méthodes pour recuperer les infos d'un abonnement"""

    def rechercher_prix_DAO(self,  abonnement: Abonnement) -> bool:
        """Cette méthode recherche les infos sur un abonnement"""

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT prix FROM abonnement             "
                    " WHERE id_abonnement = %(id_abonnement)s      ",
                    {"id_abonnement": abonnement.id_abonnement},
                )
                res = cursor.fetchone()

        prix = None
        if res:
            prix = res

        return prix


    def rechercher_pub_DAO(self,  abonnement: Abonnement) -> bool:
        """Cette méthode recherche les infos sur un abonnement"""
        
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT pub FROM abonnement             "
                    " WHERE id_abonnement = %(id_abonnement)s      ",
                    {"id_abonnement": abonnement.id_abonnement},
                )
                res = cursor.fetchone()

        pub = None
        if res:
            pub = res

        return pub
    
def rechercher_qualite_DAO(self,  abonnement: Abonnement) -> bool:
        """Cette méthode recherche les infos sur un abonnement"""
        
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT qualite FROM abonnement             "
                    " WHERE id_abonnement = %(id_abonnement)s      ",
                    {"id_abonnement": abonnement.id_abonnement},
                )
                res = cursor.fetchone()

        qualite = None
        if res:
            qualite = res

        return qualite