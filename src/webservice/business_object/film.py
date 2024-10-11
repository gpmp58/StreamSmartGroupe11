import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

def transformer_duree(d = int):
    h = d//60
    m = d % 60
    duree = f"{h} h {m} min"
    return duree



class Film():
    """Cette classe s'occupe de récupérer les différentes informations sur les films
    A continuer pour la description
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
        liste_films = {film["id"]: film["original_title"] for film in films_obtenus}
        return liste_films
        """ ne pas oublier de réfléchir à l'autocomplétion"""

    def afficher_film(self, id):
        cle_api = os.environ.get("API_KEY")
        url_search_movie = f"https://api.themoviedb.org/3/movie/{str(id)}"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {cle_api}"
        }
        response = requests.get(url_search_movie, headers=headers)
        if response.status_code == 200:
            content = json.loads(response.content)
            result = {
                "name": content["original_title"],
                "description": content["overview"],
                "sortie": content["status"],
                "vote_average": content["vote_average"],
                "date_sortie" : content["release_date"],
                "duree" : content["runtime"],
                "genres" : [genre["name"] for genre in content["genres"]]
            }
            result["duree"] = transformer_duree(content["runtime"])
            return result
        else:
            raise Exception("Le film n'a pas été trouvé (pas le bon id).")



    def recuperer_image(self,id :int):
        cle_api = os.environ.get("API_KEY")
        url_search_movie_2 = f"https://api.themoviedb.org/3/movie/{str(id)}/images"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {cle_api}"
        }
        response = requests.get(url_search_movie_2, headers=headers)
        content = json.loads(response.content)
        result = {
                "image": content['posters'][0]['file_path']

            }
        return result
# A utiliser dans streamlit pour pouvoir afficher le film

# pas de test pour les méthodes qui recherchent des infos en ligne
a = Film("Batman")
