from src.webservice.services.service_critere import CritereService
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
from src.webservice.services.service_watchlist import WatchlistService
from src.webservice.business_object.critere import Critere

if __name__ == "__main__":
    creationu = UtilisateurService().creer_compte(nom="Alice", prenom="Dupont",
            pseudo="alice123",
            adresse_mail="alice@example.com",
            mdp="password123",
            langue="français"
        )


    creation1 = WatchlistService().creer_nouvelle_watchlist("favories" ,creationu)
    creation2 = WatchlistService().creer_nouvelle_watchlist("favories2" ,creationu)
    film = Film(268)
    film2 = Film(152)
    #print(film.recuperer_streaming())
    ajoutfilm = WatchlistService().ajouter_film(film, creation1)
    ajoutfilm2 = WatchlistService().ajouter_film(film2, creation1)
    criteres = Critere(creation1, {"qualite":"4K", "pub":False, "prix":False,'rapport_quantite_prix':False})
    plateforme = CritereService().recuperer_plateformes_film(criteres)
    #print(plateforme)
    
    filtres = CritereService().filtrer_abonnement(criteres)
    #print(filtres)
    occurences = CritereService().calculer_occurrences_plateformes(criteres)
    #print(occurences)
    optimisation = CritereService().optimiser_abonnement(criteres)
    #print(optimisation)
    print( CritereService().afficher_abonnement_optimise(criteres))

