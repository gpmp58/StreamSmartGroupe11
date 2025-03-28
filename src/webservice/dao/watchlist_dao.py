from src.webservice.dao.db_connection import DBConnection
from src.webservice.business_object.watchlist import Watchlist
import logging


class WatchlistDao:
    """Classe contenant les méthodes pour accéder aux watchlists de la bdd"""

    def creer_nouvelle_watchlist_DAO(
        self, watchlist: Watchlist
    ) -> bool:
        """Crée une nouvelle watchlist dans la base de données.
        ----------
        watchlist : Watchlist
            Instance de la classe Watchlist à ajouter à la base de données.

        Returns
        -------
        bool
            True si la création est un succès, False sinon.
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(
                        "INSERT INTO projet11.watchlist "
                        "(nom_watchlist, id_utilisateur)"
                        "VALUES (%(nom_watchlist)s, %(id_utilisateur)s)      "
                        "RETURNING id_watchlist;                            ",
                        {
                            "nom_watchlist": watchlist.nom_watchlist,
                            "id_utilisateur": watchlist.id_utilisateur,
                        },
                    )
                    res = cursor.fetchone()

                    if res:
                        watchlist.id_watchlist = res["id_watchlist"]
                        return True
                    return False
                except Exception as e:
                    logging.error(
                        f"Erreur lors de la création de la watchlist : {e}"
                    )
                    return False

    def supprimer_watchlist_DAO(self, watchlist: Watchlist) -> bool:
        """Suppression d'un watchlist dans la base de données

        Parameters
        ----------
        watchlist : watchlist
            watchlist à supprimer de la base de données

        Returns
        -------
            True si le watchlist a bien été supprimé
        """

        if not watchlist.id_watchlist:
            logging.error(
                "L'identifiant de la watchlist est manquant."
            )
            return False

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        DELETE FROM projet11.watchlist
                        WHERE id_watchlist = %(id_watchlist)s
                        """,
                        {"id_watchlist": watchlist.id_watchlist},
                    )
                    res = cursor.rowcount

            if res > 0:
                logging.info(
                    f"Watchlist avec id {watchlist.id_watchlist}"
                    f" supprimée avec succès."
                )
                return True
            else:
                logging.warning(
                    f"Watchlist avec id {watchlist.id_watchlist} introuvable."
                )
                return False

        except Exception as e:
            logging.error(
                f"Erreur lors de la suppression de la watchlist : {e}"
            )
            return False

    def ajouter_film_DAO(
        self, id_watchlist: int, id_film: int
    ) -> bool:
        """Ajoute un film à une watchlist dans la base de données

        Parameters
        ----------
        id_watchlist : int
            L'identifiant de la watchlist à laquelle le film doit être ajouté
        id_film : int
            L'identifiant du film à ajouter

        Returns
        -------
        bool
            True si le film a été ajouté avec succès
            False sinon
        """
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO projet11.film_watchlist (
                        id_watchlist, id_film
                        )
                        VALUES (%(id_watchlist)s, %(id_film)s);
                        """,
                        {
                            "id_watchlist": id_watchlist,
                            "id_film": id_film,
                        },
                    )
                    res = cursor.rowcount

            if res > 0:
                logging.info(
                    f"Film {id_film} ajouté à la watchlist"
                    f" {id_watchlist} avec succès."
                )
                return True
            else:
                logging.warning(
                    f"Échec de l'ajout du film {id_film} à"
                    f" la watchlist {id_watchlist}."
                )
                return False

        except Exception as e:
            logging.error(
                f"Erreur lors de l'ajout du film {id_film} "
                f"à la watchlist {id_watchlist} : {e}"
            )
            return False

    def supprimer_film_DAO(
        self, id_watchlist: int, id_film: int
    ) -> bool:
        """Supprimer un film dans une watchlist dans la base de données

        Parameters
        ----------
        id_watchlist : int
            L'identifiant de la watchlist à laquelle le film doit être supprimé
        id_film : int
            L'identifiant du film à supprimer

        Returns
        -------
        bool
            True si le film a été ajouté avec succès
            False sinon
        """
        try:
            res = None
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM projet11.film_watchlist "
                        " WHERE id_watchlist = %(id_watchlist)s        "
                        "        AND id_film = %(id_film)s             ",
                        {
                            "id_watchlist": id_watchlist,
                            "id_film": id_film,
                        },
                    )
                    res = cursor.rowcount

            if res > 0:
                logging.info(
                    f"Film {id_film} supprimé de la "
                    f"watchlist {id_watchlist}."
                )
                return True
            else:
                logging.warning(
                    f"Aucun film trouvé avec id_film {id_film}"
                    f" dans la watchlist {id_watchlist}."
                )
                return False

        except Exception as e:
            logging.error(
                f"Erreur lors de la suppression du film {id_film}"
                f" de la watchlist {id_watchlist}: {e}"
            )
            return False

    def film_deja_present(
        self, id_watchlist: int, id_film: int
    ) -> bool:
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT COUNT(*)  "
                        " FROM projet11.film_watchlist  "
                        "WHERE id_watchlist = %(id_watchlist)s        "
                        "      AND id_film = %(id_film)s;             ",
                        {
                            "id_watchlist": id_watchlist,
                            "id_film": id_film,
                        },
                    )
                    res = cursor.fetchone()
                    logging.debug(f"Résultat de la requête : {res}")
                    if res and res["count"] > 0:
                        return True
                    return False

        except Exception as e:
            logging.error(
                f"Erreur lors de la vérification de la présence "
                f"du film {id_film} dans la watchlist {id_watchlist}: {e}"
            )
            return False

    def recuperer_films_watchlist_DAO(
        self, id_watchlist: int
    ) -> list:
        """
        Récupère tous les films d'une watchlist spécifique.
        """
        films = []
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT f.id_film, f.nom_film "
                        "FROM projet11.film_watchlist fw "
                        "JOIN projet11.film f ON fw.id_film = f.id_film "
                        "WHERE fw.id_watchlist = %(id_watchlist)s;",
                        {"id_watchlist": id_watchlist},
                    )
                    films_data = cursor.fetchall()
                    films = [
                        {
                            "id_film": film["id_film"],
                            "nom_film": film["nom_film"],
                        }
                        for film in films_data
                    ]

        except Exception as e:
            logging.error(
                f"Erreur lors de la récupération des films "
                f"pour la watchlist {id_watchlist}: {e}"
            )
        return films

    def afficher_watchlist_DAO(self, id_utilisateur: int) -> list:
        """
        Récupère toutes les watchlists pour un
        utilisateur spécifique, avec les films associés.
        Parameters
        ----------
        id_utilisateur : int
            L'identifiant de l'utilisateur dont
            on veut récupérer les watchlists
        Returns
        -------
        list
        Liste des watchlists avec les films associés pour chaque watchlist
        """
        watchlists = []
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT id_watchlist,nom_watchlist
                        FROM projet11.watchlist
                        WHERE id_utilisateur = %(id_utilisateur)s;
                        """,
                        {"id_utilisateur": id_utilisateur},
                    )
                    watchlists_data = cursor.fetchall()
                    watchlists = [
                        {
                            "id_watchlist": watchlist["id_watchlist"],
                            "nom_watchlist": watchlist[
                                "nom_watchlist"
                            ],
                        }
                        for watchlist in watchlists_data
                    ]

                    logging.info(
                        f"{len(watchlists)} watchlists récupérées"
                        f" pour l'utilisateur ID: {id_utilisateur}"
                    )
                    return watchlists
        except Exception as e:
            logging.error(
                f"Erreur lors de la récupération des watchlists "
                f"pour l'utilisateur ID: {id_utilisateur}: {str(e)}"
            )

    def verifier_film_existe(self, id_film):
        """
        Vérifie si un film existe déjà dans la base
        de données en fonction de son ID ou de son nom.

        Args:
            id_film (int) : L'identifiant du film à vérifier..

        Returns:
            bool : Retourne True si le film existe déjà, sinon False.
        """
        try:
            # Connexion à la base de données
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Exécution de la requête pour vérifier si l'id ou le nom
                    # existe déjà dans la base
                    cursor.execute(
                        "SELECT 1 FROM projet11.film WHERE id_film = %s ;",
                        (id_film,),
                    )
                    result = cursor.fetchone()

                    return result is not None

        except Exception as e:
            print(
                f"Erreur lors de la vérification du film {id_film}: {e}"
            )
            return False

    def trouver_par_id_w(self, id_watchlist: int):
        """
        Trouver un utilisateur grâce à son id.

        Parameters:
        -----------
        id_utilisateur : int
            L'ID de l'utilisateur.
        Returns:
        --------
        Utilisateur : Instance de la classe Utilisateur
            contenant les informations de l'utilisateur.
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM projet11.watchlist "
                    "WHERE id_watchlist = %(id_watchlist)s;",
                    {"id_watchlist": id_watchlist},
                )
                res = cursor.fetchone()

        if res:
            return Watchlist(
                id_utilisateur=res["id_utilisateur"],
                nom_watchlist=res["nom_watchlist"],
                id_watchlist=res["id_watchlist"],
            )
        else:
            raise ValueError("Watchlist introuvable.")
