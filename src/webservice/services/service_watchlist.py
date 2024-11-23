from src.webservice.dao.watchlist_dao import WatchlistDao
from src.webservice.business_object.watchlist import Watchlist
from src.webservice.business_object.utilisateur import Utilisateur

from src.webservice.business_object.film import Film
from src.webservice.dao.film_dao import FilmDao


import logging


class WatchlistService:
    """
    Service de gestion des watchlists. Cette classe fournit des
     méthodes pour créer, supprimer des watchlists,
    ajouter ou supprimer des films d'une watchlist,
    et gérer les mises à jour de la base de données.

    Méthodes :
        - creer_nouvelle_watchlist : Crée une nouvelle
                watchlist pour un utilisateur.
        - supprimer_watchlist : Supprime une watchlist.
        - ajouter_film : Ajoute un film dans une watchlist.
        - mise_jour_bases : Met à jour les informations
                liées au film dans les bases de données.
        - supprimer_film : Supprime un film d'une watchlist.
        - sauvegarder_watchlist :
                Sauvegarde et récupère les films d'une watchlist.
    """

    def creer_nouvelle_watchlist(
        self, nom_watchlist: str, utilisateur: Utilisateur
    ) -> Watchlist:
        """
        Crée une nouvelle watchlist pour un utilisateur.

        Cette méthode permet de créer une nouvelle watchlist
        pour l'utilisateur, en utilisant le nom de la watchlist
        et l'ID de l'utilisateur.

        Args:
            nom_watchlist (str) :
                Le nom de la nouvelle watchlist.
            utilisateur (Utilisateur) :
                L'objet utilisateur auquel la watchlist sera associée.

        Returns:
            Watchlist : L'objet `Watchlist` créé
                    si la création est réussie, sinon `None`.
        """
        if (
            not nom_watchlist
            or not utilisateur
            or not utilisateur.id_utilisateur
        ):
            logging.error(
                "Paramètres invalides pour la création de la watchlist."
            )
            return None
        nouvelle_watchlist = Watchlist(
            nom_watchlist, utilisateur.id_utilisateur
        )
        if WatchlistDao().creer_nouvelle_watchlist_DAO(
            nouvelle_watchlist
        ):
            return nouvelle_watchlist
        else:
            logging.error(
                "Échec de la création de la watchlist dans la base de données."
            )
            return None

    def supprimer_watchlist(self, watchlist: Watchlist) -> bool:
        """
        Supprime une watchlist de la base de données.

        Args:
            watchlist (Watchlist) : L'objet Watchlist à supprimer.

        Returns:
            bool : True si la suppression est réussie, sinon False.
        """
        return WatchlistDao().supprimer_watchlist_DAO(watchlist)

    def ajouter_film(self, film: Film, watchlist):
        """
        Ajoute un film à une watchlist.

        Args:
            film : L'objet Film à ajouter à la watchlist.
            watchlist (Watchlist) : L'objet Watchlist dans
                            lequel il faut ajouter le film.

        Returns:
            bool : True si le film est ajouté avec succès, sinon False.
        """
        id_film = film.id_film
        id_watchlist = watchlist.id_watchlist
        if WatchlistDao().film_deja_present(id_watchlist, id_film):
            logging.warning(
                f"Le film {id_film} est déjà dans la watchlist {id_watchlist}."
            )
            return False
        if not WatchlistDao().verifier_film_existe(id_film):
            FilmDao().ajouter_film(film)
        succes_ajout = WatchlistDao().ajouter_film_DAO(
            id_watchlist, id_film
        )

        if succes_ajout:
            logging.info(
                f"Le film {id_film} a été ajouté avec "
                f"succès à la watchlist {id_watchlist}."
            )
        else:
            logging.error(
                f"Erreur lors de l'ajout du film {id_film}"
                f" à la watchlist {id_watchlist}."
            )

        return succes_ajout

    def supprimer_film(self, Film, watchlist):
        """
        Supprime un film d'une watchlist.

        Args:
            film : L'objet Film à supprimer de la watchlist.
            watchlist (Watchlist) : L'objet Watchlist dans
                    lequelle il faut supprimer le film.

        Returns:
            bool : True si la suppression est réussie, sinon False.
        """
        id_film = Film.id_film
        id_watchlist = watchlist.id_watchlist
        deja_present = WatchlistDao().film_deja_present(
            id_watchlist, id_film
        )
        if not deja_present:
            logging.warning(
                f"Le film {id_film} n'est pas présent"
                f" dans la watchlist {id_watchlist}."
            )
            return False
        succes_suppression = WatchlistDao().supprimer_film_DAO(
            id_watchlist, id_film
        )
        return succes_suppression

    def sauvegarder_watchlist(self, watchlist):
        """
        Sauvegarde et récupère les films d'une watchlist.

        Args:
            watchlist (Watchlist) : L'objet Watchlist
                        dont les films doivent être récupérés.

        Returns:
            list : Liste des films présents dans la watchlist.
        """
        id_watchlist = watchlist.id_watchlist
        if not watchlist.id_watchlist:
            logging.error(
                "Erreur: l'identifiant de la watchlist"
                " est invalide ou manquant."
            )
            return []
        films = WatchlistDao().recuperer_films_watchlist_DAO(
            id_watchlist
        )
        watchlist.list_film = films
        return watchlist.list_film

    def afficher_watchlist(self, id_utilisateur):
        """
        Récupère et affiche la liste des watchlists d'un utilisateur donné,
         ainsi que les films associés à chaque watchlist.

        Attributs
        ----------
        id_utilisateur : L'identifiant de l'utilisateur pour lequel
                les watchlists et les films doivent être récupérés.

        Returns :
           list : Une liste de dictionnaires représentant
                les watchlists de l'utilisateur.
        """
        watchlists = []
        try:
            watchlist_data = WatchlistDao().afficher_watchlist_DAO(
                id_utilisateur
            )
            for watchlist in watchlist_data:
                id_watchlist = watchlist["id_watchlist"]
                nom_watchlist = watchlist["nom_watchlist"]
                watchlist = Watchlist(
                    nom_watchlist=nom_watchlist,
                    id_watchlist=id_watchlist,
                    id_utilisateur=id_utilisateur,
                )
                # Récupérer les films pour cette watchlist
                films = self.sauvegarder_watchlist(watchlist)

                watchlists.append(
                    {
                        "id_watchlist": id_watchlist,
                        "nom_watchlist": nom_watchlist,
                        "films": films,
                    }
                )

            return watchlists
        except Exception as e:
            logging.error(
                f"Erreur lors de la récupération des watchlists et"
                f" films pour l'utilisateur ID: {id_utilisateur} - {e}"
            )

    def trouver_par_id(self, id_watchlist):
        """cherche la watchlist à partir de son
        identifiant
        --------
        Parametres
        int
            id_watchlist
        --------
        returns
        watchlist
            Watchlist"""
        watchlist = WatchlistDao().trouver_par_id_w(id_watchlist)
        self.sauvegarder_watchlist(watchlist)
        return watchlist
