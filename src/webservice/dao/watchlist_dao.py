from src.webservice.dao.db_connection import DBConnection

from src.webservice.business_object.watchlist import Watchlist


class WatchlistDao:
    """Classe contenant les méthodes pour accéder aux watchlists de la bdd"""

    def creer_nouvelle_watchlist_DAO(self, watchlist: Watchlist) -> bool:
        """Crée une nouvelle watchlist dans la base de données.

        Parameters
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
                        "INSERT INTO watchlist (nom_watchlist, id_utilisateur)"
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
                    print(f"Erreur lors de la création de la watchlist : {e}")
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

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM watchlist                       "
                    " WHERE id_watchlist = %(id_watchlist)s      ",
                    {"id_watchlist": watchlist.id_watchlist},
                )
                res = cursor.rowcount

        return res > 0

    def ajouter_film_DAO(self, id_watchlist: int, id_film: int) -> bool:
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
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO film_watchlist(id_watchlist, id_film)    "
                    "VALUES (%(id_watchlist)s, %(id_film)s);              ",
                    {"id_watchlist": id_watchlist, "id_film": id_film},
                )
                res = cursor.rowcount

        return res > 0

    def supprimer_film_DAO(self, id_watchlist: int, id_film: int) -> bool:
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
        res = None
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM film_watchlist                    "
                    " WHERE id_watchlist = %(id_watchlist)s        "
                    "        AND id_film = %(id_film)s             ",
                    {"id_watchlist": id_watchlist, "id_film": id_film},
                )
                res = cursor.rowcount

        return res > 0

    def film_deja_present(self, id_watchlist: int, id_film: int) -> bool:
        res = None
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*)                              "
                    " FROM film_watchlist                         "
                    "WHERE id_watchlist = %(id_watchlist)s        "
                    "      AND id_film = %(id_film)s;             ",
                    {"id_watchlist": id_watchlist, "id_film": id_film},
                )
                res = cursor.fetchone()[0]

        # Si le nombre de lignes trouvées > 0, le film est déjà présent
        return res > 0

    def recuperer_films_watchlist_DAO(self, id_watchlist: int) -> list:
        """
        Récupère tous les films d'une watchlist spécifique.
        """
        films = []
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT f.id_film, f.nom "
                    "FROM film_watchlist fw "
                    "JOIN film f ON fw.id_film = f.id_film "
                    "WHERE fw.id_watchlist = %(id_watchlist)s;",
                    {"id_watchlist": id_watchlist},
                )
                films = cursor.fetchall()

        return films
