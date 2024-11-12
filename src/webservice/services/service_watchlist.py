from src.webservice.dao.watchlist_dao import WatchlistDao
from src.webservice.business_object.watchlist import Watchlist
from src.webservice.business_object.utilisateur import Utilisateur
from src.webservice.services.service_utilisateur import UtilisateurService
from src.webservice.business_object.film import Film
from src.webservice.services.service_film import FilmService
from src.webservice.dao.film_dao import FilmDao
from src.webservice.dao.plateforme_dao import PlateformeDAO
from src.webservice.services.service_plateforme import ServicePlateforme
from src.webservice.business_object.plateforme import PlateformeStreaming

import logging

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
        if not nom_watchlist or not utilisateur or not utilisateur.id_utilisateur:
            logging.error("Paramètres invalides pour la création de la watchlist.")
            return None
        id_utilisateur = utilisateur.id_utilisateur
        nouvelle_watchlist = Watchlist(nom_watchlist, utilisateur.id_utilisateur)
        if WatchlistDao().creer_nouvelle_watchlist_DAO(nouvelle_watchlist):
            return nouvelle_watchlist
        else:
            logging.error("Échec de la création de la watchlist dans la base de données.")
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

    def ajouter_film(self, film : Film, watchlist):
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
        if WatchlistDao().film_deja_present(id_watchlist, id_film):
            logging.warning(f"Le film {id_film} est déjà dans la watchlist {id_watchlist}.")
            return False
        succes_ajout_film = FilmDao().ajouter_film(film)
        if not succes_ajout_film:
            raise Exception(f"Le film {id_film} n'a pas pu être ajouté à la base de données.")
        succes_ajout = WatchlistDao().ajouter_film_DAO(id_watchlist, id_film)

        if succes_ajout:
            logging.info(f"Le film {id_film} a été ajouté avec succès à la watchlist {id_watchlist}.")
        else:
            logging.error(f"Erreur lors de l'ajout du film {id_film} à la watchlist {id_watchlist}.")
        
        return succes_ajout

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
            logging.warning(f"Le film {id_film} n'est pas présent dans la watchlist {id_watchlist}.")
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
        if not watchlist.id_watchlist:
            logging.error(f"Erreur: l'identifiant de la watchlist est invalide ou manquant.")
            return []
        films = WatchlistDao().recuperer_films_watchlist_DAO(id_watchlist)
        watchlist.list_film = films
        watchlist.list_film = films
        return watchlist.list_film
    
    

if __name__ == "__main__":
    """utilisateur = Utilisateur(
        id_utilisateur=123,
        nom="Alice",
        prenom="Dupont",
        pseudo="alice123",
        adresse_mail="alice@example.com",
        mdp="hashed_password",
        langue="français",
        sel="random_salt"
    )"""
    creationu = UtilisateurService().creer_compte(nom="Alice", prenom="Dupont",
            pseudo="alice123",
            adresse_mail="alice@example.com",
            mdp="password123",
            langue="français"
        )


    creation1 = WatchlistService().creer_nouvelle_watchlist("favories" ,creationu)
    print(creation1.id_watchlist)
    #delete = WatchlistService().supprimer_watchlist(Watchlist("favories",1,[],1))
    #print(delete)
    film = Film(268)
    print(film.recuperer_streaming())
    #print(film.details['name'])
    #ajout = FilmDao().ajouter_film(film)
    ajoutfilm = WatchlistService().ajouter_film(film, creation1)
    #present = WatchlistDao().film_deja_present(1,268)
    #print(present)
    #delete = WatchlistService().supprimer_film(film,creation1)
    liste_film = WatchlistService().sauvegarder_watchlist(creation1)
    print(liste_film)
    plateforme = ServicePlateforme().ajouter_plateforme(film)
