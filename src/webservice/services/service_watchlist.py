from src.webservice.dao.watchlist_dao import WatchlistDao
from src.webservice.business_object.watchlist import Watchlist

class WatchlistService:

    def creer_nouvelle_watchlist(self, nom_watchlist, utilisateur):
        id_utilisateur = utilisateur.id_utilisateur
        nouvelle_watchlist = Watchlist(nom_watchlist, id_utilisateur)
        return nouveau_watchlist if WatchlistDao().creer_nouvelle_watchlist_DAO(nouvelle_watchlist) else None
    
    def supprimer_watchlist(self, watchlist):
        return WatchlistDao().supprimer_watchlist_DAO(watchlist)
    
    def ajouter_film(self, Film, watchlist):
        id_film = Film.id_film
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
        id_film = film.id_film
        id_watchlist = watchlist.id_watchlist
        if self.ajouter_film(film,watchlist):
            succes_ajout_film = FilmDAO().ajouter_film(id_film)
            if succes_ajout_film :
                id_plateforme = film.donner_id_plateforme()
                nom_plateforme = film.donner_nom_plateforme()
                success_ajout_plateforme = service_plateforme().mettre_a_jour_plateforme(id_plateforme,nom_plateforme)
            else :    
                print(f"Erreur lors de l'ajout du film '{film.nom}' à la base de données.")
                return False


    def supprimer_film(self, Film, watchlist):
        id_film = Film.id_film
        id_watchlist = watchlist.id_watchlist
        deja_present = WatchlistDao().film_deja_present(id_watchlist, id_film)
        if not deja_present:
            print(f"Erreur: Le film n'est pas présent dans la watchlist.")
            return False
        succes_suppression = WatchlistDao().supprimer_film_DAO(id_watchlist, id_film)
        return succes_suppression

    def sauvegarder_watchlist(self, watchlist):
        id_watchlist = watchlist.id_watchlist
        films = WatchlistDao().recuperer_films_watchlist_DAO(id_watchlist)
        watchlist.list_film = film
        return watchlist.list_film

    
