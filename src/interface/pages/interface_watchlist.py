from InquirerPy import prompt
import requests
from src.interface.session_manager import get_session_state

# URL de base de l'API FastAPI
LIEN_API = "http://127.0.0.1:8000"

# Vérifier la connexion utilisateur
def verifier_connexion():
    session_state = get_session_state()  # Récupérer l'état de la session
    vrai_id = session_state.get("id_utilisateur")  # ID utilisateur stocké dans la session

    while True:
        id = input("Entrez votre id : ").strip()
        if not id:
            print("Erreur : Veuillez entrer un id valide.")
            continue

        # Vérification de l'ID utilisateur
        if str(vrai_id) != id:
            print("❌ L'ID tapé ne correspond pas à votre session. Veuillez réessayer.")
        else:
            return id

# Créer une nouvelle watchlist
def creer_watchlist(id):
    nom_watchlist = input("Entrez le nom de la nouvelle watchlist : ").strip()
    if not nom_watchlist:
        print("Erreur : Le nom de la watchlist est obligatoire.")
        return
    data = {"nom_watchlist": nom_watchlist, "id_utilisateur": id}
    try:
        response = requests.post(f"{LIEN_API}/watchlists", json=data)
        if response.status_code == 200:
            print("✅ Watchlist créée avec succès !")
        else:
            print(f"Erreur : {response.json().get('detail', 'ERREUR INCONNUE')}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion à l'API : {e}")

# Afficher les watchlists de l'utilisateur
def afficher_watchlists(id):
    try:
        response = requests.get(f"{LIEN_API}/watchlists/utilisateur/{id}")
        if response.status_code == 200:
            watchlists = response.json().get("watchlists", [])
            if watchlists:
                for watchlist in watchlists:
                    print(f"\n📋 {watchlist['nom_watchlist']} (ID : {watchlist['id_watchlist']})")
                    films = watchlist.get("films", [])
                    if films:
                        for film in films:
                            print(f"  - {film['nom_film']} (ID : {film['id_film']})")
                    else:
                        print("  Aucun film dans cette watchlist.")
            else:
                print("Aucune watchlist trouvée pour cet utilisateur.")
        else:
            print(f"Erreur : {response.json().get('detail', 'Erreur lors de la récupération des watchlists.')}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion à l'API : {e}")

# Ajouter un film à une watchlist
def ajouter_film():
    watchlist_id = input("Entrez le numéro de la watchlist : ").strip()
    film_id = input("Entrez le numéro du film : ").strip()
    if not watchlist_id or not film_id:
        print("Erreur : Tous les champs doivent être remplis.")
        return
    data = {"id_watchlist": watchlist_id, "id_film": film_id}
    try:
        response = requests.post(f"{LIEN_API}/watchlists/ajouter_film", json=data)
        if response.status_code == 200:
            print("✅ Film ajouté à la watchlist avec succès !")
        else:
            print(f"Erreur : {response.json().get('detail', 'ERREUR INCONNUE')}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion à l'API : {e}")

# Supprimer une watchlist
def supprimer_watchlist():
    watchlist_id = input("Entrez le numéro de la watchlist à supprimer : ").strip()
    if not watchlist_id:
        print("Erreur : Le numéro de la watchlist est obligatoire.")
        return
    try:
        response = requests.delete(f"{LIEN_API}/watchlists/{watchlist_id}")
        if response.status_code == 200:
            print("🗑️ Watchlist supprimée avec succès.")
        else:
            print(f"Erreur : {response.json().get('detail', 'Erreur lors de la suppression.')}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion à l'API : {e}")

# Supprimer un film d'une watchlist
def supprimer_film():
    watchlist_id = input("Entrez le numéro de la watchlist : ").strip()
    film_id = input("Entrez le numéro du film : ").strip()
    if not watchlist_id or not film_id:
        print("Erreur : Tous les champs doivent être remplis.")
        return
    try:
        response = requests.delete(f"{LIEN_API}/watchlists/{watchlist_id}/supprimer_film/{film_id}")
        if response.status_code == 200:
            print("✅ Film supprimé avec succès.")
        else:
            print(f"Erreur : {response.json().get('detail', 'Erreur lors de la suppression du film.')}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion à l'API : {e}")

# Récupérer les films d'une watchlist
def recuperer_films_watchlist():
    watchlist_id = input("Entrez le numéro de la watchlist : ").strip()
    if not watchlist_id:
        print("Erreur : Le numéro de la watchlist est obligatoire.")
        return
    try:
        response = requests.get(f"{LIEN_API}/watchlists/{watchlist_id}/films")
        if response.status_code == 200:
            films = response.json().get("films", [])
            if films:
                for film in films:
                    print(f"  - {film['nom_film']} (ID : {film['id_film']})")
            else:
                print("Aucun film trouvé dans cette watchlist.")
        else:
            print(f"Erreur : {response.json().get('detail', 'Erreur lors de la récupération des films.')}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion à l'API : {e}")

# Menu principal
def menu_principal(id):
    actions = {
        "1": ("Créer une Watchlist", lambda: creer_watchlist(id)),
        "2": ("Afficher les Watchlists", lambda: afficher_watchlists(id)),
        "3": ("Ajouter un Film à une Watchlist", ajouter_film),
        "4": ("Supprimer une Watchlist", supprimer_watchlist),
        "5": ("Supprimer un Film d'une Watchlist", supprimer_film),
        "6": ("Récupérer les Films d'une Watchlist", recuperer_films_watchlist),
    }

    while True:
        print("\n=== Gestion des Watchlists ===")
        for key, (label, _) in actions.items():
            print(f"{key}. {label}")
        print("7. Retourner au menu principal")

        choix = input("Choisissez une option : ").strip()
        if choix == "7":
            print("Au revoir !")
            from src.interface.pages.interface_utilisateur_connecte import main1
            main1()
        elif choix in actions:
            actions[choix][1]()
        else:
            print("Option invalide. Veuillez réessayer.")

# Programme principal
def main_watchlist():
    id = verifier_connexion()
    if id:
        menu_principal(id)

if __name__ == "__main__":
    main()
