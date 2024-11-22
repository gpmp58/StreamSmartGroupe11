from src.webservice.business_object.plateforme import PlateformeStreaming

from src.webservice.dao.db_connection import DBConnection


class PlateformeDAO:
    """
    Classe permettant d'interagir avec la base de données pour gérer les plateformes de streaming.
    """

    def ajouter_plateforme(self, plateforme: PlateformeStreaming):
        """
        Ajoute une nouvelle plateforme dans plateforme_abonnement avec un identifiant spécifique si elle n'existe pas déjà.

        Args:
            plateforme (PlateformeStreaming): Plateforme à ajouter.

        Returns:
            bool : True si la plateforme a été ajoutée avec succès, False si la plateforme existe déjà dans la base de données ou si une erreur survient.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Vérifier si la plateforme existe déjà (par id ou nom)
                    cursor.execute(
                        "SELECT COUNT(*) FROM projet11.plateforme_abonnement WHERE id_plateforme = %s OR nom_plateforme = %s;",
                        (plateforme.id_plateforme, plateforme.nom_plateforme),
                    )
                    count = cursor.fetchone()

                    if count and count["count"] > 0:
                        print(
                            f"La plateforme avec l'ID '{plateforme.id_plateforme}' ou le nom '{plateforme.nom_plateforme}' existe déjà."
                        )
                        return False

                    # Insérer la nouvelle plateforme
                    cursor.execute(
                        "INSERT INTO projet11.plateforme_abonnement (id_plateforme, nom_plateforme) VALUES (%s, %s);",
                        (plateforme.id_plateforme, plateforme.nom_plateforme),
                    )
                    print(
                        f"La plateforme '{plateforme.nom_plateforme}' a été ajoutée avec succès."
                    )
                    return True  # Plateforme ajoutée avec succès

        except Exception as e:
            print(f"Erreur lors de l'ajout de la plateforme : {e}")
            return False

    def verifier_plateforme_existe(self, id_plateforme, nom_plateforme):
        """
        Vérifie si une plateforme existe déjà dans la base de données en fonction de son ID ou de son nom.

        Args:
            id_plateforme (int) : L'identifiant de la plateforme à vérifier.
            nom_plateforme (str) : Le nom de la plateforme à vérifier.

        Returns:
            bool : Retourne True si la plateforme existe déjà, sinon False.
        """
        try:
            # Connexion à la base de données
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Exécution de la requête pour vérifier si l'id ou le nom
                    # existe déjà dans la base
                    cursor.execute(
                        "SELECT 1 FROM projet11.plateforme_abonnement WHERE id_plateforme = %s OR nom_plateforme = %s;",
                        (
                            id_plateforme,
                            nom_plateforme,
                        ),  # Paramètres pour la requête SQL
                    )
                    result = (
                        cursor.fetchone()
                    )  # Récupère le premier résultat de la requête

                    # Si un résultat existe, la plateforme existe déjà, donc on
                    # retourne True
                    # Si la requête renvoie une ligne, c'est que la plateforme
                    # existe
                    return result is not None

        except Exception as e:
            print(
                f"Erreur lors de la vérification de la plateforme {nom_plateforme}: {e}"
            )
            return False  # En cas d'erreur, on retourne False

    def ajouter_relation_film_plateforme(self, id_film, id_plateforme):
        """
        Ajoute la relation entre un film et une plateforme dans la table `film_plateforme`.

        Args:
            id_film (int): L'identifiant du film.
            id_plateforme (int): L'identifiant de la plateforme.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO projet11.film_plateforme (id_plateforme,id_film) VALUES (%s, %s);",
                        (id_plateforme, id_film),
                    )
                    print(
                        f"La relation film ({id_film}) - plateforme ({id_plateforme}) a été ajoutée."
                    )
        except Exception as e:
            print(
                f"Erreur lors de l'ajout de la relation film ({id_film}) - plateforme ({id_plateforme}): {e}"
            )
