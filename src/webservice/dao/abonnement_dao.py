from src.webservice.dao.db_connection import DBConnection
from src.webservice.business_object.abonnement import Abonnement
from src.webservice.business_object.plateforme import Plateforme


class AbonnementDao:
    """Classe avec les méthodes pour récupérer les infos d'un abonnement"""

    def get_prix_abonnement_DAO(self, abonnement: Abonnement) -> float:
        """Cette méthode renvoie le prix d'un abonnement"""
        prix = None
        try :
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT prix FROM projet11.abonnement "
                        "WHERE id_abonnement = %(id_abonnement)s",
                        {"id_abonnement": abonnement.id_abonnement},
                    )
                    prix = cursor.fetchone()
            if prix is None:
                logging.warning(f"Aucun prix trouvé pour l'abonnement ID: {abonnement.id_abonnement}")
                return None
            return prix
        except Exception as e:
            logging.error(f"Erreur lors de la récupération du prix pour l'abonnement ID: {abonnement.id_abonnement} - {e}")
            return None

    def get_pub_abonnement_DAO(self, abonnement: Abonnement) -> tuple:
        """Cette méthode renvoie true si l'abonnement fait de la pub"""
        pub = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT pub FROM projet11.abonnement "
                        "WHERE id_abonnement = %(id_abonnement)s",
                        {"id_abonnement": abonnement.id_abonnement},
                    )
                    pub = cursor.fetchone()
            if pub is None:
                logging.warning(f"Aucune information sur la publicité trouvée pour l'abonnement ID: {abonnement.id_abonnement}")
                return False
            return pub

    def get_qualite_abonnement_DAO(self, abonnement: Abonnement) -> tuple:
        """Cette méthode recherche la qualité d'un abonnement"""
        qualite = None
        try :
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT qualite FROM projet11.abonnement "
                        "WHERE id_abonnement = %(id_abonnement)s",
                        {"id_abonnement": abonnement.id_abonnement},
                    )
                    qualite = cursor.fetchone()
            if qualite is None:
                logging.warning(f"Aucune information sur la qualité trouvée pour l'abonnement ID: {abonnement.id_abonnement}")
                return None  # Aucun résultat trouvé, donc on retourne None

            return qualite 

        except Exception as e:
            logging.error(f"Erreur lors de la récupération de la qualité pour l'abonnement ID: {abonnement.id_abonnement} - {e}")
            return None

    def get_nom_abonnement_DAO(self, abonnement: Abonnement) -> tuple:
        """Cette méthode recherche le nom d'un abonnement"""
        nom = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT nom_abonnement FROM projet11.abonnement "
                        "WHERE id_abonnement = %(id_abonnement)s",
                        {"id_abonnement": abonnement.id_abonnement},
                    )
                    nom = cursor.fetchone()
                if nom is None:
                    logging.warning(f"Aucun nom trouvé pour l'abonnement ID: {abonnement.id_abonnement}")
                    return None  # Si aucun nom n'est trouvé, retourner None

                return nom  # Retourner le nom trouvé

        except Exception as e:
            logging.error(f"Erreur lors de la récupération du nom de l'abonnement ID: {abonnement.id_abonnement} - {e}")

    def get_abonnement_by_plateforme_DAO(self, plateforme: Plateforme) -> list:
        """Cette méthode fournit la liste d'abonnements d'une plateforme"""
        abonnements = []
        try :
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id_abonnement "
                        "FROM projet11.abonnement "
                        "WHERE nom_plateforme = %(nom_plateforme)s",
                        {"nom_plateforme": plateforme.nom_plateforme},
                    )
                    abonnements_data = cursor.fetchall()

            if abonnements_data:

                abonnements = [{"id_abonnement": abonnement[0]} for abonnement in abonnements_data]
            else:
                logging.warning(f"Aucun abonnement trouvé pour la plateforme: {plateforme.nom_plateforme}")

            return abonnements
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des abonnements pour la plateforme {plateforme.nom_plateforme} - {e}")
            return abonnements
