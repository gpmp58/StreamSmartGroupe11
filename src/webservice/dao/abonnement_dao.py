
from src.webservice.dao.db_connection import DBConnection

from src.webservice.business_object.abonnement import Abonnement


class AbonnementDao():
    """Classe contenant les méthodes pour recuperer les infos d'un abonnement"""

    def rechercher_info_DAO(self,  abonnement: Abonnement) -> bool:
        """Cette méthode recherche les infos sur un abonnement"""

        
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM abonnement             "
                    " WHERE id_abonnement = %(id_abonnement)s      ",
                    {"id_abonnement": abonnement.id_abonnement},
                )
                res = cursor.fetchone()

        abonnement = None
        if res:
            abonnement = Abonnement(
                prix=res["prix"],
                pub=res["pub"],
                qualite=res["qualite"],
                id_plateforme=res["id_plateforme"],
                id_abonnement=res["id_abonnement"]
            )

        return abonnement
    