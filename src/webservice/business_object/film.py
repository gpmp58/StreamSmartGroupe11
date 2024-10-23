import os
from dotenv import load_dotenv
import requests
import json
from googletrans import Translator

load_dotenv()


def transformer_duree(d=int):
    h = d // 60
    m = d % 60
    duree = f"{h} h {m} min"
    return duree


translator = Translator()

def traduire_texte(texte, target_lang="fr"):
    if not texte:
        return ""
    detection = translator.detect(texte)
    lang_source = detection.lang
    if lang_source != target_lang:
        translation = translator.translate(texte, dest=target_lang)
        return translation.text
    return texte


class Film:
    """
    Création de la classe Film.

    Cette classe permet de récupérer les infos du film en fonction de l'ID donné.
    """

    def __init__(self, id_film: int):
        self.id_film = id_film
        self.image = self.recuperer_image()
        self.streaming = self.recuperer_streaming()
        self.details = self.afficher_film()

    def afficher_film(self):
        cle_api = os.environ.get("API_KEY")
        url_search_movie = f"https://api.themoviedb.org/3/movie/{str(self.id_film)}"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {cle_api}"
        }
        response = requests.get(url_search_movie, headers=headers)
        if response.status_code == 200:
            content = json.loads(response.content)
            result = {
                "name": content["original_title"],
                "description": traduire_texte(content["overview"]),
                "sortie": content["status"],
                "vote_average": content["vote_average"],
                "date_sortie": content["release_date"],
                "duree": transformer_duree(content["runtime"]),
                "genres": [genre["name"] for genre in content["genres"]],
            }

            return result
        else:
            raise Exception("Le film n'a pas été trouvé (pas le bon id).")

    def recuperer_image(self):
        cle_api = os.environ.get("API_KEY")
        url_search_movie_2 = (
            f"https://api.themoviedb.org/3/movie/{str(self.id_film)}/images")
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {cle_api}"
        }
        response = requests.get(url_search_movie_2, headers=headers)
        content = json.loads(response.content)

        if content["posters"]:
            return ("https://image.tmdb.org/t/p/w600_and_h900_bestv2" +
                    content["posters"][0]["file_path"])
        else:
            return "Image non disponible"
        # peut-être mettre un lien d'une image qui montre qu'on a pas d'image

    def recuperer_streaming(self):
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
                streaming = dict()
                result_flatrate = result_fr["flatrate"]
                for provider in result_flatrate:
                    streaming[provider["provider_id"]] = provider["provider_name"]
                return streaming
            else:
                return "Pas disponible en streaming en France."
        else:
            return "Aucune information de streaming disponible pour ce film."
