import requests

# URL de l'API FastAPI
BASE_URL = "http://127.0.0.1:8000"  # Change si nécessaire

# Fonction pour rechercher un film par nom
def rechercher_film(nom_film):
    try:
        response = requests.post(
            f"{BASE_URL}/films/recherche", json={"nom_film": nom_film}
        )
        if response.status_code == 200:
            return response.json().get("films", {})
        else:
            return {"error": "Erreur lors de la recherche de film"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Erreur lors de la connexion à l'API : {e}"}

# Fonction pour obtenir les détails d'un film
def obtenir_details_film(id_film):
    try:
        response = requests.get(f"{BASE_URL}/films/{id_film}")
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Erreur lors de la récupération des détails du film"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Erreur lors de la connexion à l'API : {e}"}
