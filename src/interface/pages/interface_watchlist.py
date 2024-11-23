from InquirerPy import prompt
import requests
from src.interface.session_manager import get_session_state

# URL de base de l'API FastAPI
LIEN_API = "http://127.0.0.1:8000"


def verifier_connexion():
    """Vérifie l'ID utilisateur en le comparant avec l'ID dans la session."""
    session_state = get_session_state()
    vrai_id = session_state.get("id_utilisateur")

    while True:
        id = input("\nEntrez votre ID utilisateur : ").strip()
        if not id:
            print("Erreur : Veuillez entrer un ID valide.")
            continue

        if str(vrai_id) != id:
            print(
                "\n❌ L'ID tapé ne correspond pas à votre session."
                "Veuillez réessayer."
            )
        else:
            return id


def creer_watchlist(id):
    """Crée une nouvelle watchlist pour l'utilisateur."""
    nom_watchlist = input(
        "\nEntrez le nom de la nouvelle watchlist : "
    ).strip()
    if not nom_watchlist:
        print("\nErreur : Le nom de la watchlist est obligatoire.")
        return
    data = {"nom_watchlist": nom_watchlist, "id_utilisateur": id}
    try:
        response = requests.post(f"{LIEN_API}/watchlists", json=data)
        if response.status_code == 200:
            print("\n✅ Watchlist créée avec succès !")
        else:
            print("\nImpossible de créer la watchlist")
    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion à l'API : {e}")


def supprimer_film(id_utilisateur):
    """Supprime un film d'une watchlist via un menu déroulant
    pour sélectionner le film."""
    try:
        # Étape 1 : Récupérer les watchlists de l'utilisateur
        response = requests.get(
            f"{LIEN_API}/watchlists/utilisateur/{id_utilisateur}"
        )
        response.raise_for_status()
        watchlists = response.json().get("watchlists", [])
        if not watchlists:
            print("❌ Aucune watchlist trouvée.")
            return

        # Étape 2 : Choisir une watchlist
        watchlist_choices = [
            {
                "name": f"{wl['nom_watchlist']} (ID : {wl['id_watchlist']})",
                "value": wl["id_watchlist"],
            }
            for wl in watchlists
        ]
        questions_watchlist = [
            {
                "type": "list",
                "name": "id_watchlist",
                "message": "Choisissez une watchlist :",
                "choices": watchlist_choices,
            }
        ]
        watchlist_answers = prompt(questions_watchlist)
        id_watchlist = watchlist_answers["id_watchlist"]

        # Étape 3 : Récupérer les films de la watchlist
        response_films = requests.get(
            f"{LIEN_API}/watchlists/{id_watchlist}/films"
        )
        response_films.raise_for_status()
        films = response_films.json().get("films", [])
        if not films:
            print(
                f"❌ Aucun film trouvé dans la watchlist (ID : {id_watchlist})."
            )
            return

        # Étape 4 : Choisir un film
        film_choices = [
            {
                "name": f"{film['nom_film']} (ID : {film['id_film']})",
                "value": film["id_film"],
            }
            for film in films
        ]
        questions_film = [
            {
                "type": "list",
                "name": "id_film",
                "message": "Choisissez un film à supprimer :",
                "choices": film_choices,
            }
        ]
        film_answers = prompt(questions_film)
        id_film = film_answers["id_film"]

        # Étape 5 : Supprimer le film de la watchlist
        response_delete = requests.delete(
            f"{LIEN_API}/watchlists/{id_watchlist}/supprimer_film/{id_film}"
        )
        if response_delete.status_code == 200:
            print("✅ Film supprimé avec succès.")
        else:
            print(
                f"❌ Erreur : "
                f"{response_delete.json().get('detail','Erreur lors de la suppression du film.')}"
            )

    except requests.exceptions.RequestException as e:
        print(f"❌ Une erreur s'est produite : {e}")


def afficher_watchlists(id):
    """Affiche les watchlists d'un utilisateur avec leurs films."""
    try:
        # Récupérer les watchlists de l'utilisateur
        response = requests.get(
            f"{LIEN_API}/watchlists/utilisateur/{id}"
        )
        if response.status_code == 200:
            watchlists = response.json().get("watchlists", [])
            if watchlists:
                # Menu déroulant pour sélectionner une watchlist
                questions = [
                    {
                        "type": "list",
                        "name": "id_watchlist",
                        "message": "Sélectionnez une watchlist "
                        "pour voir son contenu :",
                        "choices": [
                            {
                                "name": f"{wl['nom_watchlist']}"
                                " (ID : {wl['id_watchlist']})",
                                "value": wl["id_watchlist"],
                            }
                            for wl in watchlists
                        ],
                    }
                ]
                answers = prompt(questions)
                selected_watchlist_id = answers["id_watchlist"]

                # Récupérer les films de la watchlist sélectionnée
                films_response = requests.get(
                    f"{LIEN_API}/watchlists/{selected_watchlist_id}/films"
                )
                if films_response.status_code == 200:
                    films = films_response.json().get("films", [])
                    print(
                        f"\n=== Contenu de la Watchlist "
                        f"(ID : {selected_watchlist_id}) ==="
                    )
                    if films:
                        for film in films:
                            print(
                                f"- {film['nom_film']}"
                                f" (ID : {film['id_film']})"
                            )
                    else:
                        print(
                            "  Aucun film trouvé dans cette watchlist."
                        )
                else:
                    print(
                        "Erreur : Impossible de récupérer"
                        " les films de cette watchlist."
                    )
            else:
                print(
                    "\nAucune watchlist trouvée pour cet utilisateur."
                )
        else:
            print("Impossible d'afficher les watchlists.")
    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion à l'API : {e}")


def ajouter_film(id):
    """Ajoute un film à une watchlist via une sélection."""
    from src.interface.pages.interface_utilisateur_connecte import (
        main1,
    )

    try:
        # Récupérer les watchlists de l'utilisateur
        response = requests.get(
            f"{LIEN_API}/watchlists/utilisateur/{id}"
        )
        response.raise_for_status()
        watchlists = response.json().get("watchlists", [])
        if not watchlists:
            print(
                "\n❌ Aucune watchlist trouvée. Veuillez en créer une d'abord."
            )
            print("\nRetour au menu principal.")
            main1()
            return

        # Afficher les choix des watchlists
        watchlist_choices = [
            {
                "name": f"{wl['nom_watchlist']} (ID : {wl['id_watchlist']})",
                "value": wl["id_watchlist"],
            }
            for wl in watchlists
        ]

        questions = [
            {
                "type": "list",
                "name": "id_watchlist",
                "message": "\nChoisissez une watchlist :",
                "choices": watchlist_choices,
            },
            {
                "type": "input",
                "name": "id_film",
                "message": "\nEntrez l'ID du film :",
                "validate": lambda result: result.isdigit()
                or result.lower() == "retour"
                or "Veuillez entrer un ID valide ou 'Retour'."
                or "Veuillez entrer un nombre valide.",
            },
        ]

        answers = prompt(questions)
        data = {
            "id_watchlist": answers["id_watchlist"],
            "id_film": answers["id_film"],
        }

        # Envoyer la requête pour ajouter un film à la watchlist
        response = requests.post(
            f"{LIEN_API}/watchlists/ajouter_film", json=data
        )
        if response.status_code == 200:
            print("\n✅ Film ajouté à la watchlist avec succès !")
        else:
            print("\nErreur : Film introuvable")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion à l'API : {e}")


def supprimer_watchlist(id):
    """Supprime une watchlist via une sélection."""
    try:
        response = requests.get(
            f"{LIEN_API}/watchlists/utilisateur/{id}"
        )
        response.raise_for_status()
        watchlists = response.json().get("watchlists", [])
        if not watchlists:
            print("\nAucune watchlist trouvée.")
            return

        watchlist_choices = [
            {
                "name": f"{wl['nom_watchlist']} (ID : {wl['id_watchlist']})",
                "value": wl["id_watchlist"],
            }
            for wl in watchlists
        ]

        questions = [
            {
                "type": "list",
                "name": "id_watchlist",
                "message": "Choisissez la watchlist à supprimer :",
                "choices": watchlist_choices,
            }
        ]

        answers = prompt(questions)
        watchlist_id = answers["id_watchlist"]

        response = requests.delete(
            f"{LIEN_API}/watchlists/{watchlist_id}"
        )
        if response.status_code == 200:
            print("\n Watchlist supprimée avec succès.")
        else:
            print(
                f"Erreur : {response.json().get('detail', 'Erreur inconnue')}"
            )
    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion à l'API : {e}")


def menu_principal(id):
    """Affiche le menu principal des actions disponibles."""
    actions = {
        "1": ("Créer une Watchlist", lambda: creer_watchlist(id)),
        "2": (
            "Afficher les Watchlists",
            lambda: afficher_watchlists(id),
        ),
        "3": (
            "Ajouter un Film à une Watchlist",
            lambda: ajouter_film(id),
        ),
        "4": (
            "Supprimer une Watchlist",
            lambda: supprimer_watchlist(id),
        ),
        "5": (
            "Supprimer un Film d'une Watchlist",
            lambda: supprimer_film(id),
        ),
    }

    while True:
        print("\n=== Gestion des Watchlists ===")
        for key, (label, _) in actions.items():
            print(f"{key}. {label}")
        print("\n6. Retourner au menu principal")

        choix = input("Choisissez une option : ").strip()
        if choix == "6":
            from src.interface.pages.interface_utilisateur_connecte import (
                main1,
            )

            main1()
            break
        elif choix in actions:
            actions[choix][1]()
        else:
            print("\nOption invalide. Veuillez réessayer.")


def main_watchlist():
    """Programme principal pour la gestion des watchlists."""
    id = verifier_connexion()
    if id:
        menu_principal(id)


if __name__ == "__main__":
    main_watchlist()
