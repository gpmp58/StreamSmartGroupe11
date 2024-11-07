from src.webservice.dao.watchlist_dao import WatchlistDao
from src.webservice.business_object.watchlist import Watchlist
from src.webservice.business_object.utilisateur import Utilisateur

class WatchlistService:
    """
    Service de gestion des watchlists. Cette classe fournit des méthodes pour créer, supprimer des watchlists,
    ajouter ou supprimer des films d'une watchlist, et gérer les mises à jour de la base de données.

    Méthodes :
        - creer_nouvelle_watchlist : Crée une nouvelle watchlist pour un utilisateur.
        - supprimer_watchlist : Supprime une watchlist.
        - ajouter_film : Ajoute un film dans une watchlist.
        - mise_jour_bases : Met à jour les informations liées au film dans les bases de données.
        - supprimer_film : Supprime un film d'une watchlist.
        - sauvegarder_watchlist : Sauvegarde et récupère les films d'une watchlist.
    """

    def creer_nouvelle_watchlist(self, nom_watchlist: str, utilisateur: Utilisateur) -> Watchlist:
        """
        Crée une nouvelle watchlist pour un utilisateur.

        Cette méthode permet de créer une nouvelle watchlist pour l'utilisateur, en utilisant le nom de la watchlist
        et l'ID de l'utilisateur.

        Args:
            nom_watchlist (str) : Le nom de la nouvelle watchlist.
            utilisateur (Utilisateur) : L'objet utilisateur auquel la watchlist sera associée.

        Returns:
            Watchlist : L'objet `Watchlist` créé si la création est réussie, sinon `None`.
        """
        id_utilisateur = utilisateur.id_utilisateur
        nouvelle_watchlist = Watchlist(nom_watchlist, id_utilisateur)
        return nouvelle_watchlist if WatchlistDao().creer_nouvelle_watchlist_DAO(nouvelle_watchlist) else None

    def supprimer_watchlist(self, watchlist: Watchlist) -> bool:
        """
        Supprime une watchlist de la base de données.

        Args:
            watchlist (Watchlist) : L'objet Watchlist à supprimer.

        Returns:
            bool : True si la suppression est réussie, sinon False.
        """
        return WatchlistDao().supprimer_watchlist_DAO(watchlist)

    def ajouter_film(self, film, watchlist):
        """
        Ajoute un film à une watchlist.

        Args:
            film : L'objet Film à ajouter à la watchlist.
            watchlist (Watchlist) : L'objet Watchlist dans lequel il faut ajouter le film.

        Returns:
            bool : True si le film est ajouté avec succès, sinon False.
        """
        id_film = film.id_film
        id_watchlist = watchlist.id_watchlist
        deja_present = WatchlistDao().film_deja_present(id_watchlist, id_film)
        if deja_present:
            print(f"Erreur: Le film est déjà dans la watchlist.")
            return False

        succes_ajout = WatchlistDao().ajouter_film_DAO(id_watchlist, id_film)


        if succes_ajout:
            print(f"Le film {nom_film} a été ajouté avec succès.")
        else:
            print("Erreur lors de l'ajout du film.")
        return succes_ajout

    def mise_jour_bases(self, film, watchlist):
        """
        Met à jour les informations liées au film dans les bases de données, en ajoutant le film à la watchlist, et les plateformes de streaming si nécessaire.

        Args:
            film : L'objet Film à ajouter à la watchlist.
            watchlist (Watchlist) : L'objet Watchlist dans lequel il faut ajouter le film.
        """
        id_film = film.id_film
        id_watchlist = watchlist.id_watchlist
        if self.ajouter_film(film,watchlist):
            succes_ajout_film = FilmDAO().ajouter_film(id_film)
            if succes_ajout_film :
                streaming_info = film.recuperer_streaming()
                for id_plateforme, nom_plateforme in streaming_info.items():
                    # Mettre à jour les plateformes récupérées dans la base de données
                    success_ajout_plateforme = ServicePlateforme().mettre_a_jour_plateforme(id_plateforme, nom_plateforme)


    def supprimer_film(self, Film, watchlist):
        """
        Supprime un film d'une watchlist.

        Args:
            film : L'objet Film à supprimer de la watchlist.
            watchlist (Watchlist) : L'objet Watchlist dans lequelle il faut supprimer le film.

        Returns:
            bool : True si la suppression est réussie, sinon False.
        """
        id_film = Film.id_film
        id_watchlist = watchlist.id_watchlist
        deja_present = WatchlistDao().film_deja_present(id_watchlist, id_film)
        if not deja_present:
            print(f"Erreur: Le film n'est pas présent dans la watchlist.")
            return False
        succes_suppression = WatchlistDao().supprimer_film_DAO(id_watchlist, id_film)
        return succes_suppression

    def sauvegarder_watchlist(self, watchlist):
        """
        Sauvegarde et récupère les films d'une watchlist.

        Args:
            watchlist (Watchlist) : L'objet Watchlist dont les films doivent être récupérés.

        Returns:
            list : Liste des films présents dans la watchlist.
        """
        id_watchlist = watchlist.id_watchlist
        films = WatchlistDao().recuperer_films_watchlist_DAO(id_watchlist)
        watchlist.list_film = film
        return watchlist.list_film
