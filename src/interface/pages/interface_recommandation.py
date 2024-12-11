from InquirerPy import inquirer
import requests
import os  # Import nécessaire pour nettoyer le terminal
from src.interface.session_manager import get_session_state
from src.interface.pages.interface_utilisateur_connecte import main1  # Import de main1 pour le retour

# URL de base de l'API FastAPI
LIEN_API = "http://127.0.0.1:8000"


def clear_terminal():
    """Nettoie le terminal."""
    os.system("cls" if os.name == "nt" else "clear")


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
            print(
                "❌ Erreur : L'ID tapé ne correspond"
                " pas à votre session. Veuillez réessayer."
            )
        else:
            return id_utilisateur


def demander_criteres():
    """
    Demande des critères à l'utilisateur.
    Si prix est coché Yes,
    rapport quantité/prix sera No automatiquement, et inversement
    si les deux criteres sont No , on ne prend pas en compte
    le prix comme critère
    et on cherche que la plateforme qui fournit le nombre
    de films maximal.
    """
    prix = inquirer.confirm(
        message="Souhaitez-vous le prix le plus bas ?", default=False
    ).execute()
    rapport_quantite_prix = not prix  # Inverse automatiquement le choix de prix

    qualite = inquirer.text(
        message="Qualité (ex: HD, 4K, etc.) :", default=""
    ).execute()
    pub = inquirer.confirm(
        message="Avec pub ?", default=False
    ).execute()

    return {
        "prix": prix,
        "qualite": qualite if qualite else None,
        "pub": pub,
        "rapport_quantite_prix": rapport_quantite_prix,
    }


def selectionner_watchlist(id_utilisateur):
    """Permet à l'utilisateur de sélectionner une watchlist parmi celles disponibles."""
    try:
        response = requests.get(
            f"{LIEN_API}/watchlists/utilisateur/{id_utilisateur}"
        )
        if response.status_code != 200:
            print("Erreur lors de la récupération des watchlists.")
            return None

        watchlists = response.json().get("watchlists", [])
        if not watchlists:
            print("Aucune watchlist trouvée pour cet utilisateur.")
            return None

        choix = inquirer.select(
            message="Sélectionnez une watchlist :",
            choices=[
                {
                    "name": wl["nom_watchlist"],
                    "value": wl["id_watchlist"],
                }
                for wl in watchlists
            ],
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
        response = requests.post(
            f"{LIEN_API}/plateformes_film/", json=data
        )
        if response.status_code == 200:
            result = response.json()

            # Gestion des listes vides
            for film_id, plateformes in result.items():
                if not plateformes:
                    result[film_id] = [
                        "Pas de Plateforme de Streaming disponible"
                    ]

            print("\n=== Résultat des plateformes disponibles ===")
            for film_id, plateformes in result.items():
                print(f"Film ID {film_id} : {', '.join(plateformes)}")

        else:
            print(
                f"Erreur : {response.json().get('detail', 'Erreur inconnue')}"
            )

    except Exception as e:
        print(f"Erreur de connexion à l'API : {e}")


def optimiser_et_afficher_abonnement(id_utilisateur):
    """
    Optimise l'abonnement pour une watchlist sélectionnée et affiche les résultats.
    """
    watchlist_id = selectionner_watchlist(id_utilisateur)
    if not watchlist_id:
        return

    criteres = demander_criteres()
    data = {"id_watchlist": watchlist_id, "criteres": criteres}

    try:
        print("\n🔄 Optimisation en cours...")
        # Étape 1 : Appeler la route pour optimiser l'abonnement
        response_optimiser = requests.post(
            f"{LIEN_API}/optimiser_abonnement/", json=data
        )
        if response_optimiser.status_code != 200:
            print(
                "❌ Erreur lors de l'optimisation : \n"
                "Aucun abonnement ne correspond à vos critères."
            )
            return

        # Étape 2 : Appeler la route pour afficher les détails
        print(
            "\n🔍 Récupération des détails de l'abonnement optimisé..."
        )
        response_afficher = requests.post(
            f"{LIEN_API}/afficher_abonnement_optimise/", json=data
        )
        if response_afficher.status_code == 200:
            abonnement_details = response_afficher.json().get(
                "abonnement_optimise", {}
            )
            print("\n=== Détails de l'abonnement optimisé ===")
            print(abonnement_details)
        else:
            print(
                f"❌ Erreur lors de l'affichage des détails : "
                f"{response_afficher.json().get('detail', 'Erreur inconnue')}"
            )

    except Exception as e:
        print(f"Erreur de connexion à l'API : {e}")


def menu_principal(id_utilisateur):
    """Menu principal de l'application."""
    actions = {
        "1": (
            "Accéder aux plateformes disponibles dans ma watchlist",
            lambda: recuperer_plateformes_film_watchlist(
                id_utilisateur
            ),
        ),
        "2": (
            "Trouver mon abonnement optimal",
            lambda: optimiser_et_afficher_abonnement(id_utilisateur),
        ),
        "3": ("Retour au menu principal", lambda: retour_menu_principal()),
    }

    while True:
        print("\n=== Menu Principal ===")
        for key, (label, _) in actions.items():
            print(f"{key}. {label}")

        choix = input("Choisissez une option : ").strip()
        if choix == "3":
            retour_menu_principal()
            break
        elif choix in actions:
            actions[choix][1]()
        else:
            print("Option invalide. Veuillez réessayer.")


def retour_menu_principal():
    """Fonction pour nettoyer le terminal et retourner au menu principal."""
    clear_terminal()  # Nettoie le terminal avant de retourner au menu principal
    main1()


def main_recommandation():
    """Programme principal."""
    id_utilisateur = verifier_connexion()
    if id_utilisateur:
        menu_principal(id_utilisateur)


if __name__ == "__main__":
    main_recommandation()
