from InquirerPy import inquirer
import requests
from src.interface.session_manager import get_session_state
from src.interface.pages.interface_utilisateur_connecte import (
    main1,
)  # Import de main1 pour le retour

# URL de base de l'API FastAPI
LIEN_API = "http://127.0.0.1:8000"


def verifier_connexion():
    """Vérifie l'ID utilisateur en le comparant avec l'ID dans la session."""
    session_state = get_session_state()
    vrai_id = session_state.get(
        "id_utilisateur"
    )  # Récupérer l'ID utilisateur depuis la session

    while True:
        id_utilisateur = input(
            "Entrez votre ID utilisateur : "
        ).strip()
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
    - Si prix est coché Yes, rapport quantité/prix sera No automatiquement.
    - Si les deux (prix et rapport quantité/prix) sont No :
    le critère prix est ignoré.
    On cherche ainsi uniquement la plateforme qui fournit
    le nombre maximal de films.
    """
    # Demander le critère prix
    prix = inquirer.confirm(
        message="Souhaitez-vous le prix le plus bas ?", default=False
    ).execute()

    # Si prix est "No", demander rapport quantité/prix
    rapport_quantite_prix = False
    if not prix:
        rapport_quantite_prix = inquirer.confirm(
            message="Voulez-vous un bon rapport quantité/prix ?", default=False
        ).execute()

    # Si les deux sont "No", ignorer le critère prix
    if not prix and not rapport_quantite_prix:
        print(
            "\n💡 Aucun critère prix sélectionné. "
            "Seules les plateformes avec le nombre maximal"
            "de films seront considérées.\n"
            )
        return {
            "prix": False,
            "qualite": None,
            "pub": None,
            "rapport_quantite_prix": False,
        }

    # Demander les autres critères
    qualite = inquirer.text(
        message="Qualité (ex: HD, 4K, etc.) :", default=""
    ).execute()
    pub = inquirer.confirm(
        message="Filtrer par absence de publicité ?", default=False
    ).execute()

    return {
        "prix": prix,
        "qualite": qualite if qualite else None,
        "pub": pub,
        "rapport_quantite_prix": rapport_quantite_prix,
    }


def selectionner_watchlist(id_utilisateur):
    """Permet à l'utilisateur de sélectionner une
    watchlist parmi celles disponibles."""
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


def optimiser_et_afficher_abonnement(id_utilisateur):
    """
    Optimise l'abonnement pour une watchlist
    sélectionnée et affiche les résultats.
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
                f"❌ Erreur lors de l'optimisation : "
                f"{response_optimiser.json().get('detail', 'Erreur inconnue')}"
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


def recuperer_plateformes_film_watchlist(id_utilisateur):
    """
    Affiche les plateformes disponibles pour les films d'une watchlist.
    """
    watchlist_id = selectionner_watchlist(id_utilisateur)
    if not watchlist_id:
        return

    try:
        # Dictionnaire de critères vide
        criteres = {
            "prix": None,
            "qualite": None,
            "pub": None,
            "rapport_quantite_prix": None,
        }

        # Données pour la requête
        data = {
            "id_watchlist": watchlist_id,
            "criteres": criteres,
        }

        # Requête POST vers la route `/plateformes_film/`
        response = requests.post(f"{LIEN_API}/plateformes_film/", json=data)

        if response.status_code == 200:
            # Résultat des plateformes par film
            plateformes_par_film = response.json()

            if not plateformes_par_film:
                print("\nAucune plateforme trouvée pour cette watchlist.")
                return

            print("\n=== Plateformes disponibles par film ===")
            for film_id, plateformes in plateformes_par_film.items():
                plateformes_display = (
                    ", ".join(plateformes)
                    if plateformes
                    else "Aucune plateforme disponible"
                )
                print(f"- Film ID {film_id} : {plateformes_display}")

        else:
            print(
                f"❌ Erreur : {response.json().get('detail', 'Inconnue')}"
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
        "3": ("Retour au menu principal", lambda: main1()),
    }

    while True:
        print("\n=== Menu Principal ===")
        for key, (label, _) in actions.items():
            print(f"{key}. {label}")

        choix = input("Choisissez une option : ").strip()
        if choix == "3":
            main1()
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
    main_recommandation()
