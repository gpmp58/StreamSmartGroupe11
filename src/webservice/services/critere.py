
class critere():

    def __init__(self, watchlist, criteres):

        self.watchlist = watchlist
        self.criteres = criteres
    
    def recuperer_films_plateformes(self):
        films = watchlist.list_film
        id_films = [film["id_film"] for film in films]
        films_s = []
        for film in id_films:
            film_ab = Film(film)
            film_ab.recuperer_streaming()
