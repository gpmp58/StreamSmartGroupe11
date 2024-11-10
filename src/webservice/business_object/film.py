import os
from dotenv import load_dotenv
import requests
import json
from datetime import datetime


load_dotenv()


def transformer_duree(d=int):
    """
    Transforme une durée exprimée en minutes en un format lisible heures et minutes.

    Args:
        d (int) : La durée en minutes à convertir.

    Returns:
        str : La durée sous forme de chaîne de caractères au format "X h Y min", où X est le nombre d'heures et Y le nombre de minutes.
    """
    h = d // 60
    m = d % 60
    duree = f"{h} h {m} min"
    return duree


def transformer_date(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%d/%m/%Y")


class Film:
    """
    Création de la classe Film.

    Cette classe permet de récupérer les infos du film en fonction de l'ID donné.

    Attributs
    ----------
    id_film : int
        Identifiant du film.
    """
    def __init__(self, id_film: int):
        self.id_film = id_film
        self.image = self.recuperer_image()
        self.streaming = self.recuperer_streaming()
        self.details = self.afficher_film()

    def afficher_film(self):
        """
        Récupère les informations d'un film à partir de l'API de The Movie Database (TMDb) en utilisant l'identifiant du film.

        Returns:
            dict : Un dictionnaire contenant les informations du film avec les clés suivantes :
            - "name" : Le titre original du film.
            - "description" : Un résumé du film.
            - "vote_average" : La note moyenne du film sur TMDb.
            - "date_sortie" : La date de sortie du film.
            - "duree" : La durée du film transformée à l'aide de la méthode transformer_duree.
            - "genres" : Liste des genres du film.

    Raises:
        Exception : Si la requête échoue (code de statut HTTP différent de 200), l'identifiant n'est pas le bon.
    """
        cle_api = os.environ.get("API_KEY")
        url_search_movie = f"https://api.themoviedb.org/3/movie/{str(self.id_film)}?language=fr-FR"
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
                "date_sortie": transformer_date(content["release_date"]),
                "duree": transformer_duree(content["runtime"]),
                "genres": [genre["name"] for genre in content["genres"]],
            }

            return result

    def recuperer_image(self):
        """
        Récupère l'URL de l'image du film à partir de l'API de The Movie Database (TMDb).

        Returns:
            str: L'URL du poster du film si disponible, sinon le message "Image non disponible".
        """
        cle_api = os.environ.get("API_KEY")
        url_search_movie_2 = f"https://api.themoviedb.org/3/movie/{str(self.id_film)}/images"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {cle_api}"
        }
        response = requests.get(url_search_movie_2, headers=headers)
        content = json.loads(response.content)

        # Vérifie si la clé "posters" existe et qu'il y a au moins un poster
        if "posters" in content and content["posters"]:
            return "https://image.tmdb.org/t/p/w600_and_h900_bestv2" + content["posters"][0]["file_path"]
        else:
            return "Image non disponible"


    def recuperer_streaming(self):
        """
        Récupère les services de streaming disponibles pour un film en France à partir de l'API de The Movie Database (TMDb).

        Returns:
            list : Une liste de dictionnaires avec les informations des services de streaming disponibles en France.

        """
        cle_api = os.environ.get("API_KEY")
        url_movie_providers = (
            f"https://api.themoviedb.org/3/movie/{self.id_film}/watch/providers"
        )
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {cle_api}"
        }

        response = requests.get(url_movie_providers, headers=headers)
        data = json.loads(response.content)

        if "results" in data and "FR" in data["results"]:
            result_fr = data["results"]["FR"]
            if "flatrate" in result_fr.keys():
                streaming = []
                result_flatrate = result_fr["flatrate"]
                for provider in result_flatrate:
                    streaming.append({
                        "id": provider["provider_id"],  # Ajoute l'ID du provider
                        "name": provider["provider_name"],
                        "logo" : "https://image.tmdb.org/t/p/w780" + provider["logo_path"]
                    })
                return streaming  # Renvoie une liste de services de streaming disponibles
