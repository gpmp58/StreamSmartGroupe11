def get_providers_for_movie(movie_name: str):
    url_search_movie = f"https://api.themoviedb.org/3/search/movie?query={movie_name}&include_adult=false&language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {cle_api}"
    }
    response = requests.get(url_search_movie, headers=headers)

    data = json.loads(response.content)
    premier_resultat = data["results"][0]
    movie_id = premier_resultat["id"]

    url_movie_providers = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers"

    response = requests.get(url_movie_providers, headers=headers)

    data = json.loads(response.content)

    result_fr = data["results"]["FR"]

    liste_providers = []
    if "flatrate" in result_fr.keys():
        result_flatrate = result_fr["flatrate"]
        for provider in result_flatrate:
            liste_providers.append(provider["provider_name"])

    return liste_providers