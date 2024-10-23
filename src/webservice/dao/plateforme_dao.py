from src.webservice.business_object.plateforme import PlateformeStreaming
from src.webservice.dao.db_connection import DBConnection


class PlateformeDAO:
    def ajouter_plateforme(self, plateforme: PlateformeStreaming):
        """
        Ajoute une nouvelle plateforme dans la base de données avec un identifiant spécifique.

        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Vérifier si la plateforme existe déjà (par id ou nom)
                    cursor.execute(
                        "SELECT COUNT(*) FROM projet11.plateforme WHERE id_plateforme = %s OR nom_plateforme = %s;",
                        (plateforme.id_plateforme, plateforme.nom_plateforme),
                    )
                    count = cursor.fetchone()[0]

                    if count > 0:
                        print(
                            f"La plateforme avec l'ID '{plateforme.id_plateforme}' ou le nom '{plateforme.nom_plateforme}' existe déjà."
                        )
                        return False

                    # Insérer la nouvelle plateforme
                    cursor.execute(
                        "INSERT INTO projet11.plateforme (id_plateforme, nom_plateforme) VALUES (%s, %s);",
                        (plateforme.id_plateforme, plateforme.nom_plateforme),
                    )
                    print(
                        f"La plateforme '{plateforme.nom_plateforme}' a été ajoutée avec succès."
                    )
                    return True  # Plateforme ajoutée avec succès

        except Exception as e:
            print(f"Erreur lors de l'ajout de la plateforme : {e}")
            return False
