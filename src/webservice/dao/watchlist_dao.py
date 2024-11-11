from src.webservice.dao.db_connection import DBConnection
from src.webservice.business_object.watchlist import Watchlist
import logging


class WatchlistDao:
    """Classe contenant les méthodes pour accéder aux watchlists de la bdd"""

    def creer_nouvelle_watchlist_DAO(self, watchlist: Watchlist) -> bool:
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
                        "INSERT INTO projet11.watchlist (nom_watchlist, id_utilisateur)"
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
                    logging.error(f"Erreur lors de la création de la watchlist : {e}")
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
            logging.error("L'identifiant de la watchlist est manquant.")
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
                logging.info(f"Watchlist avec id {watchlist.id_watchlist} supprimée avec succès.")
                return True
            else:
                logging.warning(f"Watchlist avec id {watchlist.id_watchlist} introuvable.")
                return False

        except Exception as e:
            logging.error(f"Erreur lors de la suppression de la watchlist : {e}")
            return False

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
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO projet11.film_watchlist (id_watchlist, id_film)
                        VALUES (%(id_watchlist)s, %(id_film)s);
                        """,
                        {"id_watchlist": id_watchlist, "id_film": id_film},
                    )
                    res = cursor.rowcount

            if res > 0:
                logging.info(f"Film {id_film} ajouté à la watchlist {id_watchlist} avec succès.")
                return True
            else:
                logging.warning(f"Échec de l'ajout du film {id_film} à la watchlist {id_watchlist}.")
                return False

        except Exception as e:
            logging.error(f"Erreur lors de l'ajout du film {id_film} à la watchlist {id_watchlist} : {e}")
            return False

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
        try:
            res = None
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM projet11.film_watchlist                    "
                        " WHERE id_watchlist = %(id_watchlist)s        "
                        "        AND id_film = %(id_film)s             ",
                        {"id_watchlist": id_watchlist, "id_film": id_film},
                    )
                    res = cursor.rowcount

            if res > 0:
                logging.info(f"Film {id_film} supprimé de la watchlist {id_watchlist}.")
                return True
            else:
                logging.warning(f"Aucun film trouvé avec id_film {id_film} dans la watchlist {id_watchlist}.")
                return False

        except Exception as e:
            logging.error(f"Erreur lors de la suppression du film {id_film} de la watchlist {id_watchlist}: {e}")
            return False

    def film_deja_present(self, id_watchlist: int, id_film: int) -> bool:
<<<<<<< HEAD

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT COUNT(*)                              "
                        " FROM projet11.film_watchlist                         "
                        "WHERE id_watchlist = %(id_watchlist)s        "
                        "      AND id_film = %(id_film)s;             ",
                        {"id_watchlist": id_watchlist, "id_film": id_film},
                    )
                    res = cursor.fetchone()
                    logging.debug(f"Résultat de la requête : {res}")
                    if res and res['count'] > 0:
                        return True

                # Si COUNT(*) > 0, cela signifie que le film est présent dans la watchlist
                    return False

        except Exception as e:
            logging.error(f"Erreur lors de la vérification de la présence du film {id_film} dans la watchlist {id_watchlist}: {e}")
            return False
=======
        res = None
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT COUNT(*) AS count
                    FROM projet11.film_watchlist
                    WHERE id_watchlist = %(id_watchlist)s
                    AND id_film = %(id_film)s;
                    """,
                    {"id_watchlist": id_watchlist, "id_film": id_film},
                )
                result = cursor.fetchone()
                if result and 'count' in result:
                    count = int(result['count'])  # Conversion explicite en entier
                    return count > 0
        return False
>>>>>>> b18ed612abb4048d4f90227aae27f862d8d3e196

    def recuperer_films_watchlist_DAO(self, id_watchlist: int) -> list:
        """
        Récupère tous les films d'une watchlist spécifique.
        """
        films = []
<<<<<<< HEAD
<<<<<<< HEAD
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
                    films = [{"id_film": film['id_film'], "nom_film": film['nom_film']} for film in films_data]

        except Exception as e:
            logging.error(f"Erreur lors de la récupération des films pour la watchlist {id_watchlist}: {e}")
=======
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
                
                films = [{"id_film": film[0], "nom": film[1]} for film in films_data]
>>>>>>> b18ed612abb4048d4f90227aae27f862d8d3e196

        return films

    def afficher_watchlist_DAO(self, id_utilisateur: int) -> list:
        """
        Récupère toutes les watchlists pour un utilisateur spécifique, avec les films associés.

        Parameters
        ----------
        id_utilisateur : int
            L'identifiant de l'utilisateur dont on veut récupérer les watchlists

        Returns
        -------
        list
            Liste des watchlists avec les films associés pour chaque watchlist
        """
        watchlists = []
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT w.id_watchlist, w.nom_watchlist, f.id_film, f.nom_film
                    FROM projet11.watchlist w
                    LEFT JOIN projet11.film_watchlist fw ON w.id_watchlist = fw.id_watchlist
                    LEFT JOIN projet11.film f ON fw.id_film = f.id_film
                    WHERE w.id_utilisateur = %(id_utilisateur)s;
                    """,
                    {"id_utilisateur": id_utilisateur},
                )
                results = cursor.fetchall()

                # Organisation des résultats pour grouper les films par watchlist
                watchlist_dict = {}
                for row in results:
                    id_watchlist = row['id_watchlist']
                    nom_watchlist = row['nom_watchlist']
                    id_film = row['id_film']
                    nom_film = row['nom_film']

                    # Si la watchlist n'existe pas encore dans le dictionnaire, on l'ajoute
                    if id_watchlist not in watchlist_dict:
                        watchlist_dict[id_watchlist] = {
                            "id_watchlist": id_watchlist,
                            "nom_watchlist": nom_watchlist,
                            "films": []
                        }

                    # Si un film est associé, on l'ajoute à la liste des films de la watchlist
                    if id_film and nom_film:
                        watchlist_dict[id_watchlist]["films"].append({
                            "id_film": id_film,
                            "nom_film": nom_film
                        })

                # Transformer le dictionnaire en liste pour faciliter l'utilisation
                watchlists = list(watchlist_dict.values())

        return watchlists
        return films
    def afficher_watchlist_DAO(self, id_utilisateur: int) -> list:
        """
        Récupère toutes les watchlists pour un utilisateur spécifique, avec les films associés.

        Parameters
        ----------
        id_utilisateur : int
            L'identifiant de l'utilisateur dont on veut récupérer les watchlists

        Returns
        -------
        list
            Liste des watchlists avec les films associés pour chaque watchlist
        """
        watchlists = []
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT w.id_watchlist, w.nom_watchlist, f.id_film, f.nom_film
                    FROM projet11.watchlist w
                    LEFT JOIN projet11.film_watchlist fw ON w.id_watchlist = fw.id_watchlist
                    LEFT JOIN projet11.film f ON fw.id_film = f.id_film
                    WHERE w.id_utilisateur = %(id_utilisateur)s;
                    """,
                    {"id_utilisateur": id_utilisateur},
                )
                results = cursor.fetchall()

                # Organisation des résultats pour grouper les films par watchlist
                watchlist_dict = {}
                for row in results:
                    id_watchlist = row['id_watchlist']
                    nom_watchlist = row['nom_watchlist']
                    id_film = row['id_film']
                    nom_film = row['nom_film']

                    # Si la watchlist n'existe pas encore dans le dictionnaire, on l'ajoute
                    if id_watchlist not in watchlist_dict:
                        watchlist_dict[id_watchlist] = {
                            "id_watchlist": id_watchlist,
                            "nom_watchlist": nom_watchlist,
                            "films": []
                        }

                    # Si un film est associé, on l'ajoute à la liste des films de la watchlist
                    if id_film and nom_film:
                        watchlist_dict[id_watchlist]["films"].append({
                            "id_film": id_film,
                            "nom_film": nom_film
                        })

                # Transformer le dictionnaire en liste pour faciliter l'utilisation
                watchlists = list(watchlist_dict.values())

        return watchlists
