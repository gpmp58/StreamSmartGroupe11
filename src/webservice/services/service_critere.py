from src.webservice.business_object.critere import Critere
from src.webservice.business_object.film import Film
from src.webservice.services.service_watchlist import WatchlistService
from src.webservice.dao.abonnement_dao import AbonnementDao

class ServiceCritere():
 
    def recuperer_plateformes_film(self,critere : Critere):
        watchlist_critere = critere.watchlist
        films = WatchlistService().sauvegarder_watchlist(watchlist)
        id_films = [film["id_film"] for film in films]
        films_et_plateformes = {}

        for id_film in id_films:
            film_critere = Film(id_film)
            plateformes = film_critere.recuperer_streaming()
            nom_plateformes = [plateforme['name'] for plateforme in plateformes]
            films_et_plateformes[id_film] = nom_plateformes

        return films_et_plateformes
    
    def filtrer_abonnement(self,critere :Critere):
        preferences = critere.criteres
        abonnement_filtrees = AbonnementDao().abonnement_filtrés(preferences)
        return abonnement_filtrees

    def calculer_occurrences_plateformes(criteres:Critere):
        abonnements_filtres = self.filtrer_abonnement(criteres)
        films_et_plateformes = self.recuperer_plateformes_film(criteres)
        occurrences_plateformes = 0
        plateformes_filtrees = {abonnement['nom_plateforme'] for abonnement in abonnements_filtres}

        for id_film, plateformes in films_et_plateformes.items():
            for plateforme in plateformes:
                if plateforme in plateformes_filtrees:
                    occurrences_plateformes[plateforme] += 1
        return dict(occurrences_plateformes)

    def optimiser_abonnement(critere : Critere):
        """
        Optimise le choix d'abonnement en fonction des critères sélectionnés par l'utilisateur.

        """
        abonnements_filtres = self.filtrer_abonnement(criteres)
        films_et_plateformes = self.recuperer_plateformes_film(criteres)
        occurances_plateformes = self.calculer_occurrences_plateformes(criteres)
        preferences = critere.criteres
        if preferences.get('prix', False):
            plateforme_optimisee = min(abonnements_filtres, key=lambda x: next(
                (abonnement['prix'] for abonnement in abonnements_filtres if abonnement['nom_plateforme'] == x['nom_plateforme']), float('inf')))
        
        elif preferences.get('rapport_qualite_prix', False):
            plateforme_optimisee = None
            meilleur_rapport = float('inf')
            
            for plateforme in abonnements_filtres:
                nom_plateforme = plateforme['nom_plateforme']

                if nom_plateforme in occurrences_plateformes and occurrences_plateformes[nom_plateforme] > 0:
                    prix_plateforme = next(abonnement['prix'] for abonnement in abonnements_filtres if abonnement['nom_plateforme'] == nom_plateforme)
                    quantite_films = occurrences_plateformes[nom_plateforme]
                    rapport = prix_plateforme / quantite_films

                    if rapport < meilleur_rapport:
                        meilleur_rapport = rapport
                        plateforme_optimisee = plateforme
            
        else:
            logging.warning("Aucune préférence de prix ou rapport spécifiée.")
            return None
        return plateforme_optimisee