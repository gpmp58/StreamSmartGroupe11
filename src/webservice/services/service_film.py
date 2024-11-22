from src.webservice.business_object.film import Film
import os
from dotenv import load_dotenv
import requests
import json


class FilmService:
    """
    Création de la classe FilmService.

    Cette classe permet de récupérer l'id du film en fonction du nom que
    l'utilisateur a rentré.

    Methods
    -------

    rechercher_film : dict
        Affiche une liste de film en fonction du nom écrit
    selectionner_film :

    """

    def __init__(self, nom_film: str = None):
        """
        Constructeur de la classe FilmService.

        Cette méthode initialise l'attribut nom_film.

        Attributs
        ----------
        nom_film : str, optionnel
            Le nom du film à rechercher via l'API TMDb.
        """

        if not isinstance(nom_film, str):
            raise TypeError("Le film doit être en format caractères")
        for caractere in nom_film:
            if not (caractere.isalnum() or caractere ==
                    " " or caractere == "&"):
                raise Exception(
                    "Il y a des caratères spéciaux dans le film, Veuillez réécrire le nom du film"
                )
        self.nom_film = nom_film

    def rechercher_film(self):
        """
        Recherche des films correspondant au nom du film spécifié à l'instanciation de l'objet.

        Returns :
            dict : Dictionnaire contenant les identifiants des films (en tant que clés) et leurs titres originaux (en tant que valeurs).
        """
        cle_api = os.environ.get("API_KEY")
        url_recherche_film = f"https://api.themoviedb.org/3/search/movie?query={self.nom_film}&include_adult=false&language=en-US&page=1"
        headers = {"accept": "application/json",
                   "Authorization": f"Bearer {cle_api}"}

        reponse = requests.get(
            url_recherche_film, headers=headers, verify=False)
        if reponse.status_code != 200:
            return {"error": "Erreur lors de la récupération des films."}
        data = json.loads(reponse.content)
        films_obtenus = data["results"]
        liste_films = dict()
        liste_films = {film["id"]: film["original_title"]
                       for film in films_obtenus}
        return liste_films


if __name__ == "__main__":
    film = FilmService("Batman").rechercher_film
    print(film)
