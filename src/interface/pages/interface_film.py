from InquirerPy import prompt
import requests
from src.interface.session_manager import get_session_state
from src.webservice.services.service_watchlist import WatchlistService
from src.webservice.services.service_plateforme import ServicePlateforme
from src.webservice.business_object.watchlist import Watchlist
from src.webservice.business_object.film import Film

# URL de base de l'API FastAPI
LIEN_API = "http://127.0.0.1:8000"

# Fonction pour tronquer le texte
def tronquer_texte(texte, max_longueur):
    if len(texte) > max_longueur:
        return texte[:max_longueur] + "..."
    return texte

# Fonction pour récupérer et afficher les watchlists de l'utilisateur
def selectionner_watchlist():
    """
    Permet à l'utilisateur de sélectionner une watchlist parmi celles disponibles.
    Retourne l'ID de la watchlist sélectionnée.
    """
    from src.interface.main_interface import main
    session_state = get_session_state()
    id_utilisateur = session_state.get("id_utilisateur")

    if not id_utilisateur:
        print("❌ Vous devez être connecté pour voir vos watchlists.")
        main()

    try:
        # Appeler la route pour récupérer les watchlists de l'utilisateur
        response = requests.get(f"{LIEN_API}/watchlists/utilisateur/{id_utilisateur}")
        response.raise_for_status()  # Vérifie les erreurs HTTP
        watchlists = response.json().get("watchlists", [])

        if not watchlists:
            print("❌ Vous n'avez pas encore de watchlists. Créez-en une avant d'ajouter des films.")
            main()

        # Afficher les watchlists disponibles
        print("\n=== Vos Watchlists ===")
        choix_watchlists = [
            {"name": f"ID: {wl['id_watchlist']} - Nom: {wl['nom_watchlist']}", "value": wl["id_watchlist"]}
            for wl in watchlists
        ]

        # Permettre à l'utilisateur de choisir une watchlist
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
        main()

# Fonction pour ajouter un film à une watchlist
def ajouter_a_watchlist(film_id):
    """
    Ajoute un film à une watchlist sélectionnée par l'utilisateur, ou en crée une nouvelle.
    """
    # Étape 1 : Sélectionner ou créer une watchlist
    id_watchlist = selectionner_watchlist()
    if not id_watchlist:
        print("💡 Astuce : Vous pouvez d'abord créer une watchlist depuis votre interface.")
        main()  # Retour au menu principal

    try:
        # Étape 2 : Créer un objet Watchlist
        watchlist = Watchlist(
            nom_watchlist="",  # Récupérer le nom si nécessaire
            id_utilisateur=0,  # Ajoutez l'utilisateur si nécessaire
            id_watchlist=id_watchlist
        )

        # Étape 3 : Créer un objet Film
        film = Film(id_film=film_id)
        nom_film = film.details["name"]  # Récupérer les détails du film
        print(f"Ajout du film : {nom_film}")

        # Étape 4 : Ajouter le film à la watchlist
        succes_ajout = WatchlistService().ajouter_film(film=film, watchlist=watchlist)
        if not succes_ajout:
            print(f"❌ Le film (ID: {film_id}) est déjà présent dans la watchlist (ID: {id_watchlist}).")
            return

        print(f"✅ Film ajouté à la watchlist (ID: {id_watchlist}).")

        # Étape 5 : Associer le film à ses plateformes : Juste la route à appeler.
        streaming_info = film.recuperer_streaming()
        for plateforme in streaming_info:
            id_plateforme = plateforme.get("id")
            nom_plateforme = plateforme.get("name")

            if not id_plateforme or not nom_plateforme:
                print("❌ Informations de plateforme incomplètes.")
                continue

            # Mise à jour ou ajout de la plateforme
            success_plateforme = ServicePlateforme().mettre_a_jour_plateforme(nom_plateforme, id_plateforme)
            if success_plateforme:
                print(f"✅ Plateforme '{nom_plateforme}' ajoutée ou mise à jour.")
            else:
                print(f"La Plateforme '{nom_plateforme}' existe déjà.")

            # Associer le film à la plateforme
            ServicePlateforme().ajouter_plateforme(film)

        print("✅ Association des plateformes au film réussie.")

    except Exception as e:
        print(f"❌ Erreur interne : {e}")

# Fonction pour afficher les détails d'un film
def afficher_details_film(film_id):
    try:
        # Récupérer les détails du film depuis l'API
        details_url = f"{LIEN_API}/films/{film_id}"
        response = requests.get(details_url)
        response.raise_for_status()
        film = response.json()

        # Afficher les détails du film
        print("\n=== Détails du Film ===")
        print(f"Nom : {film.get('name', 'Titre non disponible')}")
        print(f"Description : {film.get('description', 'Pas de description disponible.')}")
        print(f"Date de sortie : {film.get('date_sortie', 'Date non disponible')}")
        print(f"Durée : {film.get('duree', 'Durée non disponible')}")
        print(f"Genres : {', '.join(film.get('genres', ['Pas de genres disponibles']))}")
        print("\n")

        # Demander si l'utilisateur souhaite ajouter à la watchlist
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
            print("Retour au menu principal")
            from src.interface.pages.interface_utilisateur_connecte import main1
            main1()
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération des détails du film : {e}")

# Fonction pour rechercher des films
def rechercher_films(nom_film):
    try:
        # Endpoint pour rechercher des films
        url = f"{LIEN_API}/films/recherche"
        response = requests.post(url, json={"nom_film": nom_film})
        response.raise_for_status()
        films = response.json().get("films", {})

        if films:
            print("\n=== Résultats de recherche ===")
            for film_id, film_name in films.items():
                print(f"\nID: {film_id} | Nom: {film_name}")
        else:
            print("Aucun film trouvé avec ce nom.")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'appel API : {e}")

# Fonction principale pour gérer la recherche et les détails
def page_recherche_films():
    print("=== Recherche de films ===")

    while True:
        try:
            # Collecte du nom du film
            questions = [
                {
                    "type": "input",
                    "name": "nom_film",
                    "message": "Entrez le nom du film :",
                    "validate": lambda result: len(result) > 0 or "Le champ 'Nom du film' est obligatoire.",
                }
            ]

            answers = prompt(questions)
            nom_film = answers["nom_film"]

            # Appeler la fonction de recherche
            rechercher_films(nom_film)

            # Demander l'ID pour afficher les détails
            questions = [
                {
                    "type": "input",
                    "name": "film_id",
                    "message": "Entrez l'ID d'un film pour voir ses détails :",
                    "validate": lambda result: result.isdigit() or "Veuillez entrer un nombre valide.",
                }
            ]

            film_id = int(prompt(questions)["film_id"])
            afficher_details_film(film_id)

        except Exception as e:
            print(f"❌ Une erreur s'est produite : {e}")
            continue  # Ne pas arrêter, permet de continuer à interagir avec l'application

if __name__ == "__main__":
    page_recherche_films()
