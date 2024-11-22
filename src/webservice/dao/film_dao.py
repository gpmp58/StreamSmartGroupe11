from src.webservice.business_object.film import Film

from src.webservice.dao.db_connection import DBConnection


class FilmDao:
    """
    Classe permettant d'interagir avec la base de données pour gérer les films.
    """

    def ajouter_film(self, film: Film) -> bool:
        """
        Ajoute un film dans la base de données si ce dernier n'est pas déjà présent.

        Args:
            film (Film) : Film à ajouter.

        Returns:
            bool : True si le film a été ajouté avec succès, False si le film est déjà présent dans la base de données ou en cas d'erreur.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Vérifier si le film est déjà présent
                    """cursor.execute(
                        "SELECT COUNT(*) FROM projet11.film WHERE id_film = %s;", (film.id_film,)
                    )
                    count = cursor.fetchone()[0]
                    print(f"Nombre d'occurrences du film dans la base : {count}")

                    if count > 0:
                        print(
                            f"Le film '{film.details['name']}' est déjà présent dans la base de données."
                        )
                        return False  # Film déjà présent"""

                    # Ajouter le film
                    cursor.execute(
                        "INSERT INTO projet11.film (id_film, nom_film) VALUES (%s, %s);",
                        (film.id_film, film.details["name"]),
                    )
                    print(
                        f"Le film '{film.details['name']}' a été ajouté avec succès.")
                    return True

        except Exception as e:
            print(f"Une erreur est survenue lors de l'ajout du film : {e}")
            # print(f"Détails du film : id_film={film.id_film}, nom={film.details.get('name', 'Nom manquant')}")
            return False
