from InquirerPy import inquirer
import requests
from src.interface.session_manager import get_session_state
from src.interface.pages.interface_utilisateur_connecte import main1  # Import de main1 pour le retour

# URL de base de l'API FastAPI
LIEN_API = "http://127.0.0.1:8000"

def verifier_connexion():
    """Vérifie l'ID utilisateur en le comparant avec l'ID dans la session."""
    session_state = get_session_state()
    vrai_id = session_state.get("id_utilisateur")  # Récupérer l'ID utilisateur depuis la session

    while True:
        id_utilisateur = input("Entrez votre ID utilisateur : ").strip()
        if not id_utilisateur:
            print("❌ Erreur : L'ID utilisateur est obligatoire.")
            continue

        if str(vrai_id) != id_utilisateur:
            print("❌ Erreur : L'ID tapé ne correspond pas à votre session. Veuillez réessayer.")
        else:
            return id_utilisateur

def demander_criteres():
    """
    Demande des critères à l'utilisateur.
    Si prix est coché Yes, rapport quantité/prix sera No automatiquement, et inversement.
    """
    prix = inquirer.confirm(message="Filtrer par prix ?", default=False).execute()
    rapport_quantite_prix = not prix  # Inverse automatiquement le choix de prix

    qualite = inquirer.text(message="Qualité (ex: HD, 4K, etc.) :", default="").execute()
    pub = inquirer.confirm(message="Filtrer par absence de publicité ?", default=False).execute()

    return {
        "prix": prix,
        "qualite": qualite if qualite else None,
        "pub": pub,
        "rapport_quantite_prix": rapport_quantite_prix,
    }

def selectionner_watchlist(id_utilisateur):
    """Permet à l'utilisateur de sélectionner une watchlist parmi celles disponibles."""
    try:
        response = requests.get(f"{LIEN_API}/watchlists/utilisateur/{id_utilisateur}")
        if response.status_code != 200:
            print("Erreur lors de la récupération des watchlists.")
            return None

        watchlists = response.json().get("watchlists", [])
        if not watchlists:
            print("Aucune watchlist trouvée pour cet utilisateur.")
            return None

        choix = inquirer.select(
            message="Sélectionnez une watchlist :",
            choices=[{"name": wl["nom_watchlist"], "value": wl["id_watchlist"]} for wl in watchlists],
        ).execute()
        return choix

    except Exception as e:
        print(f"Erreur de connexion à l'API : {e}")
        return None

def recuperer_plateformes_film_watchlist(id_utilisateur):
    """
    Récupère les plateformes disponibles dans une watchlist et gère les listes vides.
    """
    watchlist_id = selectionner_watchlist(id_utilisateur)
    if not watchlist_id:
        return

    criteres = demander_criteres()
    data = {"id_watchlist": watchlist_id, "criteres": criteres}
    try:
        response = requests.post(f"{LIEN_API}/plateformes_film/", json=data)
        if response.status_code == 200:
            result = response.json()

            # Gestion des listes vides
            for film_id, plateformes in result.items():
                if not plateformes:
                    result[film_id] = ["Pas de Plateforme de Streaming disponible"]

            print("\n=== Résultat des plateformes disponibles ===")
            for film_id, plateformes in result.items():
                print(f"Film ID {film_id} : {', '.join(plateformes)}")

        else:
            print(f"Erreur : {response.json().get('detail', 'Erreur inconnue')}")

    except Exception as e:
        print(f"Erreur de connexion à l'API : {e}")

def optimiser_abonnement(id_utilisateur):
    """
    Trouve l'abonnement optimal pour une watchlist sélectionnée par l'utilisateur.
    """
    watchlist_id = selectionner_watchlist(id_utilisateur)
    if not watchlist_id:
        return

    criteres = demander_criteres()
    data = {"id_watchlist": watchlist_id, "criteres": criteres}
    try:
        # Appeler la route pour récupérer l'abonnement optimisé
        response = requests.post(f"{LIEN_API}/afficher_abonnement_optimise/", json=data)
        
        if response.status_code == 200:
            print("\n=== Résultat : Abonnement Optimal ===")
            result = response.json().get("abonnement_optimise", None)

            if not result:
                print("❌ Aucun abonnement optimal trouvé pour les critères sélectionnés.")
            else:
                # Afficher les détails de l'abonnement
                for abonnement, details in result.items():
                    print(f"\n🎬 Plateforme : {abonnement}")
                    for key, value in details.items():
                        print(f"  {key.capitalize()} : {value}")
        else:
            print(f"Erreur : {response.json().get('detail', 'Erreur inconnue')}")

    except Exception as e:
        print(f"Erreur de connexion à l'API : {e}")


def menu_principal(id_utilisateur):
    """Menu principal de l'application."""
    actions = {
        "1": ("Accéder aux plateformes disponibles dans ma watchlist", lambda: recuperer_plateformes_film_watchlist(id_utilisateur)),
        "4": ("Trouver mon abonnement optimal", lambda: optimiser_abonnement(id_utilisateur)),
        "5": ("Retour au menu principal.", lambda: main1()),  # Retour à main1()
    }

    while True:
        print("\n=== Menu Principal ===")
        for key, (label, _) in actions.items():
            print(f"{key}. {label}")

        choix = input("Choisissez une option : ").strip()
        if choix == "5":
            print("Retour au menu principal utilisateur connecté.")
            main1()  # Retourne au menu utilisateur connecté
            break
        elif choix in actions:
            actions[choix][1]()
        else:
            print("Option invalide. Veuillez réessayer.")

def main_recommandation():
    """Programme principal."""
    id_utilisateur = verifier_connexion()
    if id_utilisateur:
        menu_principal(id_utilisateur)

if __name__ == "__main__":
    print("Bienvenue dans le système de recommandation de films et d'abonnements !")
    main_recommandation()
