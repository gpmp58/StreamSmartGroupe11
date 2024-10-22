from src.webservice.business_object.film import Film


class FilmDao:
    def ajouter_film(self, film: Film) -> bool:
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Vérifier si le film est déjà présent
                    cursor.execute(
                        "SELECT COUNT(*) FROM film WHERE id_film = %s;", (film.id_film)
                    )
                    count = cursor.fetchone()[0]

                    if count > 0:
                        print(
                            f"Le film '{film.nom}' est déjà présent dans la base de données."
                        )
                        return False  # Film déjà présent

                    # Ajouter le film
                    cursor.execute(
                        "INSERT INTO film (id_film, nom) VALUES (%s, %s);",
                        (film.id_film, film.nom),
                    )
                    print(f"Le film '{film.nom}' a été ajouté avec succès.")
                    return True

        except Exception as e:
            print(f"Une erreur est survenue lors de l'ajout du film : {e}")
            return False
