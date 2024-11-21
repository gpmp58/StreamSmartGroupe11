from src.webservice.business_object.critere import Critere
from src.webservice.business_object.film import Film
from src.webservice.services.service_watchlist import WatchlistService
from src.webservice.dao.abonnement_dao import AbonnementDao
from src.webservice.business_object.abonnement import Abonnement
import logging

class CritereService():
 
    def recuperer_plateformes_film(self,critere : Critere):
        id_watchlist = critere.id_watchlist
        watchlist_critere = WatchlistService().trouver_par_id(id_watchlist)
        films = WatchlistService().sauvegarder_watchlist(watchlist_critere)
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

    def calculer_occurrences_plateformes(self, criteres:Critere):
        abonnements_filtres = self.filtrer_abonnement(criteres)
        films_et_plateformes = self.recuperer_plateformes_film(criteres)
        occurrences_plateformes = {}
        plateformes_filtrees = {abonnement['nom_plateforme'] for abonnement in abonnements_filtres}
        print(plateformes_filtrees)
        for plateformes in films_et_plateformes.values():  # Récupère les listes de plateformes
            for plateforme in plateformes:  # Parcourt chaque plateforme
                if plateforme in plateformes_filtrees:
                    if plateforme not in occurrences_plateformes:
                        occurrences_plateformes[plateforme] = 0
                    occurrences_plateformes[plateforme] += 1

        return occurrences_plateformes



    def optimiser_abonnement(self,critere : Critere):
        """
        Optimise le choix d'abonnement en fonction des critères sélectionnés par l'utilisateur.

        """
        abonnements_filtres = self.filtrer_abonnement(critere)
        films_et_plateformes = self.recuperer_plateformes_film(critere)
        occurrences_plateformes = self.calculer_occurrences_plateformes(critere)
        preferences = critere.criteres
        if preferences.get('prix', False):
            # Cas où on utilise le critère de prix et d'occurrences > 0
            plateforme_optimisee = min(
                abonnements_filtres,
                key=lambda x: (
                    next(
                        (abonnement['prix'] for abonnement in abonnements_filtres 
                        if abonnement['nom_plateforme'] == x['nom_plateforme'] and occurrences_plateformes.get(x['nom_plateforme'], 0) > 0),
                        float('inf')
                    )
                )
            )
        
        elif preferences.get('rapport_quantite_prix', False):
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
            plateforme_optimisee = max(
                abonnements_filtres,
                key=lambda x: occurrences_plateformes.get(x['nom_plateforme'], 0)
            )
        abonnement_optimise = Abonnement(
        id_abonnement=plateforme_optimisee['id_abonnement'],
        nom_plateforme=plateforme_optimisee['nom_plateforme'],
    )

        return abonnement_optimise
    
    def afficher_abonnement_optimise(self,criteres):
        """
        Résume de manière élégante les informations d'un abonnement optimisé.
        """
        abonnement = self.optimiser_abonnement(criteres)
        if abonnement:
            return (
                f"Abonnement optimisé :\n"
                f"- Plateforme : {abonnement.nom_plateforme}\n"
                f"- ID de l'abonnement : {abonnement.id_abonnement}\n"
                f"- Prix : {abonnement.prix:.2f} €"
            )
        else:
            return "Aucun abonnement optimisé trouvé."