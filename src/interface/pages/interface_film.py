from InquirerPy import prompt
import requests
from src.interface.session_manager import get_session_state

# URL de base de l'API FastAPI
LIEN_API = "http://127.0.0.1:8000"


def tronquer_texte(texte, max_longueur):
    """Tronque un texte à une longueur maximale."""
    if len(texte) > max_longueur:
        return texte[:max_longueur] + "..."
    return texte


def selectionner_watchlist():
    """Sélectionne une watchlist à partir des données utilisateur."""
    from src.interface.main_interface import main

    session_state = get_session_state()
    id_utilisateur = session_state.get("id_utilisateur")

    if not id_utilisateur:
        print("❌ Vous devez être connecté pour voir vos watchlists.")
        main()

    try:
        response = requests.get(f"{LIEN_API}/watchlists/utilisateur/{id_utilisateur}")
        response.raise_for_status()
        watchlists = response.json().get("watchlists", [])

        if not watchlists:
            print(
                "❌ Vous n'avez pas encore de watchlists. Créez-en une avant d'ajouter des films."
            )
            from src.interface.pages.interface_utilisateur_connecte import main1

            main1()

        print("\n=== Vos Watchlists ===")
        choix_watchlists = [
            {
                "name": f"ID: {wl['id_watchlist']} - Nom: {wl['nom_watchlist']}",
                "value": wl["id_watchlist"],
            }
            for wl in watchlists
        ]

        questions = [
            {
                "type": "list",
                "name": "id_watchlist",
                "message": "Choisissez une watchlist :",
                "choices": choix_watchlists,
            }
        ]
        answers = prompt(questions)
        return answers["id_watchlist"]

    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de la récupération des watchlists : {e}")
        from src.interface.pages.interface_utilisateur_connecte import main1

        main1()


def ajouter_a_watchlist(film_id):
    """Ajoute un film à une watchlist."""
    id_watchlist = selectionner_watchlist()
    if not id_watchlist:
        print(
            "💡 Astuce : Vous pouvez d'abord créer une watchlist depuis votre interface."
        )
        from src.interface.main_interface import main

        main()

    try:
        ajout_response = requests.post(
            f"{LIEN_API}/watchlists/ajouter_film",
            json={"id_watchlist": id_watchlist, "id_film": film_id},
        )
        if ajout_response.status_code == 200:
            print(f"✅ Film (ID: {film_id}) ajouté à la watchlist (ID: {id_watchlist}).")
        else:
            print(
                f"❌ Erreur lors de l'ajout du film : {ajout_response.json().get('detail', 'Erreur inconnue')}"
            )
            return

    except requests.exceptions.RequestException as e:
        print(f"❌ Une erreur s'est produite lors de l'ajout du film : {e}")
        return

    try:
        plateformes_response = requests.post(
            f"{LIEN_API}/films/ajouter_plateformes", json={"id_film": film_id}
        )
        if plateformes_response.status_code == 200:
            print(
                f"✅ Les plateformes pour le film (ID: {film_id}) ont été associées avec succès."
            )
        else:
            print(
                f"❌ Erreur lors de l'association des plateformes : {plateformes_response.json().get('detail', 'Erreur inconnue')}"
            )

    except requests.exceptions.RequestException as e:
        print(
            f"❌ Une erreur s'est produite lors de l'association des plateformes : {e}"
        )


def afficher_details_film(film_id):
    """Affiche les détails d'un film en vérifiant l'existence de son ID."""
    try:
        details_url = f"{LIEN_API}/films/{film_id}"
        response = requests.get(details_url)

        if response.status_code == 404:
            print(f"❌ Le film avec l'ID {film_id} n'existe pas.")
            return

        film = response.json()

        print("\n=== Détails du Film ===")
        print(f"Nom : {film.get('name', 'Titre non disponible')}")
        print(
            f"Description : {film.get('description', 'Pas de description disponible.')}"
        )
        print(f"Date de sortie : {film.get('date_sortie', 'Date non disponible')}")
        print(f"Durée : {film.get('duree', 'Durée non disponible')}")
        print(
            f"Genres : {', '.join(film.get('genres', ['Pas de genres disponibles']))}"
        )
        print("\n")

        questions = [
            {
                "type": "confirm",
                "name": "add_to_watchlist",
                "message": "Voulez-vous ajouter ce film à votre watchlist ?",
                "default": False,
            }
        ]
        answers = prompt(questions)
        if answers["add_to_watchlist"]:
            ajouter_a_watchlist(film_id)
        else:
            print("Retour au menu de recherche de films.")
            page_recherche_films()
    except requests.exceptions.RequestException as e:
        print(f"❌ Une erreur s'est produite lors de la récupération des détails : {e}")


def afficher_films_pagination(films):
    """Affiche les résultats de recherche avec pagination."""
    films_items = list(films.items())
    total_films = len(films_items)
    films_par_page = 5
    total_pages = (total_films + films_par_page - 1) // films_par_page

    page = 0
    while True:
        start_index = page * films_par_page
        end_index = min(start_index + films_par_page, total_films)
        films_page = films_items[start_index:end_index]

        print(f"\n=== Résultats de recherche : Page {page + 1}/{total_pages} ===\n")
        for film_id, film_name in films_page:
            print(f"ID: {film_id} | Nom: {film_name}")

        options = [
            "Sélectionner un film",
            "Page suivante",
            "Page précédente",
            "Retour au menu principal",
        ]
        if page == 0:
            options.remove("Page précédente")
        if page == total_pages - 1:
            options.remove("Page suivante")

        action = prompt(
            [
                {
                    "type": "list",
                    "name": "action",
                    "message": "\nQue souhaitez-vous faire ?",
                    "choices": options,
                }
            ]
        )["action"]

        if action == "Page suivante":
            page += 1
        elif action == "Page précédente":
            page -= 1
        elif action == "Sélectionner un film":
            questions = [
                {
                    "type": "input",
                    "name": "film_id",
                    "message": "Entrez l'ID d'un film pour voir ses détails (ou tapez 'Retour' pour revenir au menu principal) :",
                    "validate": lambda result: result.isdigit()
                    or result.lower() == "retour"
                    or "Veuillez entrer un ID valide ou 'Retour'.",
                }
            ]
            film_id_input = prompt(questions)["film_id"]
            if film_id_input.lower() == "retour":
                from src.interface.pages.interface_utilisateur_connecte import main1

                main1()
                return None
            return int(film_id_input)
        elif action == "Retour au menu principal":
            from src.interface.pages.interface_utilisateur_connecte import main1

            main1()
            return None


def rechercher_films(nom_film):
    """Recherche un film par son nom."""
    try:
        url = f"{LIEN_API}/films/recherche"
        response = requests.post(url, json={"nom_film": nom_film})
        response.raise_for_status()
        films = response.json().get("films", {})

        if films:
            film_id = afficher_films_pagination(films)
            if film_id is not None:
                afficher_details_film(film_id)
        else:
            print("Aucun film trouvé avec ce nom.")
    except Exception as e:
        print(f"❌ Une erreur s'est produite lors de la recherche des films : {e}")


def page_recherche_films():
    """Page principale pour rechercher un film."""
    print("=== Recherche de films ===")

    while True:
        try:
            questions = [
                {
                    "type": "input",
                    "name": "nom_film",
                    "message": "Entrez le nom du film (ou tapez 'Retour' pour revenir au menu principal) :",
                    "validate": lambda result: len(result) > 0
                    or "Le champ 'Nom du film' est obligatoire.",
                }
            ]

            answers = prompt(questions)
            nom_film = answers["nom_film"]
            if nom_film.lower() == "retour":
                from src.interface.pages.interface_utilisateur_connecte import main1

                main1()
                return

            rechercher_films(nom_film)

        except Exception as e:
            print(f"❌ Une erreur s'est produite : {e}")
            continue


if __name__ == "__main__":
    page_recherche_films()
