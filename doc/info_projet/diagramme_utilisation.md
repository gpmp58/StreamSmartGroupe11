# Diagramme de cas d'utilisation

```mermaid
  graph TD

    %% Définition des cas d'utilisation
    utilisateur[Utilisateur]
        gestion_utilisateurs["Gestion des utilisateurs"]
            %% Définition des cas d'utilisation spécifiques
            creer_compte["Créer un compte"]
            se_connecter["Se connecter"]
            supprimer_compte["Supprimer un compte"]
        gestion_watchlist["Gestion de la watchlist"]
            creer_watchlist["Créer une watchlist"]
            ajouter_film["Ajouter un film"]
            supprimer_watchlist["Supprimer une watchlist"]
        recherche_films["Recherche de films/séries"]
            rechercher_film["Rechercher un film/série"]
            voir_plateformes["Voir plateformes"]
8        gestion_criteres["Gestion des critères d'abonnement"]
                choisir_options["Choisir des options (pub, résolution)"]
        gestion_abonnements_complexes["Gestion des abonnements complexes"]
    administrateur[Administrateur]
        recommandation_abonnement["Recommandation d’abonnement"]
            analyser_watchlist["Analyser la watchlist"]
            proposer_abonnement["Proposer un abonnement"]
        gestion_localisation["Gestion de la localisation"]
            adapter_recommandations["Adapter recommandations selon pays"]

    %% Relations entre les cas d'utilisation
    utilisateur --> gestion_utilisateurs
        gestion_utilisateurs --> creer_compte
        gestion_utilisateurs --> se_connecter
        gestion_utilisateurs --> supprimer_compte
    utilisateur --> gestion_watchlist
        gestion_watchlist --> creer_watchlist
        gestion_watchlist --> ajouter_film
        gestion_watchlist --> supprimer_watchlist
    utilisateur --> recherche_films
        recherche_films --> rechercher_film
        recherche_films --> voir_plateformes
    utilisateur --> gestion_criteres
        gestion_criteres --> choisir_options
    administrateur --> recommandation_abonnement
        recommandation_abonnement --> analyser_watchlist
        recommandation_abonnement --> proposer_abonnement
    administrateur --> gestion_localisation
        gestion_localisation --> adapter_recommandations
    administrateur --> gestion_abonnements_complexes
```
