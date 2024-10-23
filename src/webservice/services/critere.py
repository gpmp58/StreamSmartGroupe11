
class critere():

    def __init__(self, watchlist, criteres):

        self.watchlist = watchlist
        self.criteres = criteres
    
    def recuperer_plateformes_film(self):

        films = watchlist.list_film
        id_films = [film["id_film"] for film in films]
        films_et_plateformes = {}

        for id_film in id_films:
            film_ab = Film(id_film)
            plateformes = film_ab.recuperer_streaming()

            noms_plateformes = [nom_plateforme for _, nom_plateforme in plateformes.items()]

            films_et_plateformes[id_film] = noms_plateformes

        return films_et_plateformes

    def 

    
