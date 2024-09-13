import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()


class Film():
    """
    """

    def __init__(self, nom_film: str):
        self.nom_film = nom_film

    def rechercher_film(self):
        cle_api = os.environ.get("API_KEY")
        url_recherche_film = f"https://api.themoviedb.org/3/search/movie?query={self.nom_film}&include_adult=false&language=en-US&page=1"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {cle_api}"
        }
        reponse = requests.get(url_recherche_film, headers=headers)
        data = json.loads(reponse.content)
        films_obtenus = data["results"]
        liste_films = dict()
        for i in range(len(films_obtenus)):
            liste_films[films_obtenus[i]["id"]] = films_obtenus[i]["original_title"]
        print(liste_films)


test = Film("batman")
test.rechercher_film()
