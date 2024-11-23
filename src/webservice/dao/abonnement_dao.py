from src.webservice.dao.db_connection import DBConnection
import logging


class AbonnementDao:
    """Classe avec les méthodes pour récupérer les infos d'un abonnement"""

    def get_prix_abonnement_DAO(self, id_abonnement):
        """Cette méthode renvoie le prix d'un abonnement
        en parcourant la base de données abonnement
        ----------
        parametres :
        int
            identifiant d'abonnement

        --------
        returns
        int
            prix d'abonnement
        """
        prix = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT prix FROM projet11.abonnement "
                        "WHERE id_abonnement = %(id_abonnement)s",
                        {"id_abonnement": id_abonnement},
                    )
                    prix = cursor.fetchone()
            if prix is not None and "prix" in prix:
                prix = float(prix["prix"])
            if prix is None:
                logging.warning(
                    f"Aucun prix trouvé pour l'abonnement ID: {id_abonnement}"
                )
                return None
            return prix
        except Exception as e:
            logging.error(
                f"Erreur lors de la récupération du prix"
                f" pour l'abonnement ID: {id_abonnement} - {e}"
            )
            return None

    def get_pub_abonnement_DAO(self, id_abonnement):
        """Cette méthode renvoie true si l'abonnement fait de la pub
                en parcourant la base de données abonnement
        ----------
        parametres :
        int
            identifiant d'abonnement

        --------
        returns
        bool
            si l'abonnement contient un pub"""
        pub = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT pub FROM projet11.abonnement "
                        "WHERE id_abonnement = %(id_abonnement)s",
                        {"id_abonnement": id_abonnement},
                    )
                    pub = cursor.fetchone()
            if pub is not None and "pub" in pub:
                pub = pub["pub"]
            if pub is None:
                logging.warning(
                    f"Aucune information sur la publicité trouvée"
                    f" pour l'abonnement ID: {id_abonnement}"
                )
                return False
            return pub
        except Exception as e:
            logging.error(
                f"Erreur lors de la récupération du pub"
                f" de l'abonnement ID:{id_abonnement} - {e}"
            )

    def get_qualite_abonnement_DAO(self, id_abonnement):
        """Cette méthode recherche la qualité d'un abonnement
                en parcourant la base de données abonnement
        ----------
        parametres :
        int
            identifiant d'abonnement

        --------
        returns
        str
            qualite d'abonnement"""
        qualite = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT qualite FROM projet11.abonnement "
                        "WHERE id_abonnement = %(id_abonnement)s",
                        {"id_abonnement": id_abonnement},
                    )
                    qualite = cursor.fetchone()
            if qualite is not None and "qualite" in qualite:
                qualite = qualite["qualite"]
            if qualite is None:
                logging.warning(
                    f"Aucune information sur la qualité "
                    f"trouvée pour l'abonnement ID: {id_abonnement}"
                )
            return qualite
        except Exception as e:
            logging.error(
                f"Erreur lors de la récupération de la qualite"
                f" de l'abonnement ID:{id_abonnement} - {e}"
            )

    def get_nom_abonnement_DAO(self, id_abonnement):
        """Cette méthode recherche le nom d'un abonnement
                en parcourant la base de données abonnement
        ----------
        parametres :
        int
            identifiant d'abonnement

        --------
        returns
        str
            nom d'abonnement"""
        nom = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT nom_abonnement FROM projet11.abonnement "
                        "WHERE id_abonnement = %(id_abonnement)s",
                        {"id_abonnement": id_abonnement},
                    )
                    nom = cursor.fetchone()
                if nom is not None and "nom_abonnement" in nom:
                    nom = nom["nom_abonnement"]
                if nom is None:
                    logging.warning(
                        f"Aucun nom trouvé pour "
                        f"l'abonnement ID: {id_abonnement}"
                    )
                    return None  # Si aucun nom n'est trouvé, retourner None

                return nom  # Retourner le nom trouvé

        except Exception as e:
            logging.error(
                f"Erreur lors de la récupération du nom"
                f" de l'abonnement ID: {id_abonnement} - {e}"
            )

    def get_abonnement_by_plateforme_DAO(self, nom_plateforme):
        """Cette méthode fournit la liste d'abonnements d'une plateforme
        à partir de la base abonnement
        ----------
        parametres :
        str
            nom_plateforme

        --------
        returns
        dict
            dictionnaire d'abonnement de la
            plateforme"""
        abonnements = []
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id_abonnement "
                        "FROM projet11.abonnement "
                        "WHERE nom_plateforme = %(nom_plateforme)s",
                        {"nom_plateforme": nom_plateforme},
                    )
                    abonnements_data = cursor.fetchall()

            if abonnements_data:
                abonnements = [
                    {"id_abonnement": abonnement["id_abonnement"]}
                    for abonnement in abonnements_data
                ]
            else:
                logging.warning(
                    f"Aucun abonnement trouvé pour"
                    f" la plateforme: {nom_plateforme}"
                )

            return abonnements
        except Exception as e:
            logging.error(
                f"Erreur lors de la récupération des abonnements"
                f" pour la plateforme {nom_plateforme} - {e}"
            )
            return abonnements

    def abonnement_filtrés(self, preferences: dict):
        """
        Récupère les abonnements filtrés sous forme de dictionnaire
        selon les préférences spécifiées par l'utilisateur.
                en parcourant la base de données abonnement
        ----------
        parametres :
        dict
            les criteres

        --------
        returns
        dict
            dictionnaire d'abonnement filtrées
            en s'appyant sur les criteres fournis
        """
        try:
            qualite_map = {"HD": 1, "4K": 2}
            qualite_valeur = qualite_map.get(
                preferences["qualite"], 0
            )
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id_abonnement, nom_plateforme, prix "
                        "FROM projet11.abonnement "
                        "WHERE pub = %s "
                        "AND (CASE "
                        "   WHEN qualite = 'HD' THEN 1 "
                        "   WHEN qualite = '4K' THEN 2 "
                        "   ELSE 0 "
                        "END) >= %s "
                        "ORDER BY prix ASC;",
                        (preferences["pub"], qualite_valeur),
                    )
                    abonnements_filtres = cursor.fetchall()
                    abonnements_list = [
                        {
                            "id_abonnement": row["id_abonnement"],
                            "nom_plateforme": row["nom_plateforme"],
                            "prix": row["prix"],
                        }
                        for row in abonnements_filtres
                    ]
                    return abonnements_list
        except Exception as e:
            logging.error(
                f"Erreur lors de la récupération des abonnements filtrés: {e}"
            )
            return None
