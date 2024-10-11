
from dao.db_connection import DBConnection

from business_object.watchlist import watchlist


class watchlistDao():
    """Classe contenant les méthodes pour accéder aux watchlists de la base des données"""

    
    def creer(self, watchlist) -> bool:
        """Creation d'un watchlist dans la base de données

        Parameters
        ----------
        watchlist : watchlist

        Returns
        -------
        created : bool
            True si la création est un succès
            False sinon
        """

        res = None

        
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO watchlist(nom) VALUES "
                    "(%(nom)s) "
                    "  RETURNING id_watchlist;",
                    {
                        "nom": watchlist.nom,
                    },
                )
                res = cursor.fetchone()

        created = False
        if res:
            id_watchlist = res["id_watchlist"]
            created = True

        return created

    
    def supprimer(self, watchlist) -> bool:
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
                    "DELETE FROM watchlist             "
                    " WHERE id_watchlist = %(id_watchlist)s      ",
                    {"id_watchlist": watchlist.id_watchlist},
                )
                res = cursor.rowcount

        return res > 0