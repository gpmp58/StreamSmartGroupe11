import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

cle_api = os.environ.get("API_KEY")


def search_film(titre: str):
    movie_name = titre
    url = f"https://api.themoviedb.org/3/search/movie?query={movie_name}&include_adult=false&language=en-US&page=1"
    headers = {"accept": "application/json", "Authorization": f"Bearer {cle_api}"}

    response = requests.get(url, headers=headers)
    data = json.loads(response.content)
    liste_film = []
    for film in data["results"]:
        if film["original_title"] == titre:
            liste_film.append(titre)
            liste_film.append(film["id"])
        return liste_film
