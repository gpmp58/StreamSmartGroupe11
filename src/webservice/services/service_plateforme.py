from src.webservice.business_object.plateforme import (
    PlateformeStreaming,
)
from src.webservice.dao.plateforme_dao import PlateformeDAO
from src.webservice.business_object.film import Film


class ServicePlateforme:
    """
    Service de gestion des plateformes de streaming.
    Fournit des méthodes pour mettre à jour ou ajouter des plateformes
    dans la base de données.
    """

    def mettre_a_jour_plateforme(self, nom_plateforme, id_plateforme):
        """
        Met à jour ou ajoute une nouvelle plateforme de streaming
        dans la base de données.

        Args:
            id_plateforme (int): L'identifiant de la plateforme de streaming.
            nom_plateforme (str): Le nom de la plateforme de streaming.

        Returns:
            bool: True si la plateforme a été ajoutée avec succès,
                  False si elle existe déjà.
        """
        try:
            plateforme_existante = (
                PlateformeDAO().verifier_plateforme_existe(
                    id_plateforme, nom_plateforme
                )
            )

            if plateforme_existante:
                print(f"La plateforme {nom_plateforme} existe déjà.")
                return False

            nouvelle_plateforme = PlateformeStreaming(
                nom_plateforme, id_plateforme
            )
            return PlateformeDAO().ajouter_plateforme(
                nouvelle_plateforme
            )

        except Exception as e:
            print(f"Erreur lors de l'ajout de {nom_plateforme}: {e}")
            return False

    def ajouter_plateforme(self, film: Film):
        """
        Ajoute des plateformes de streaming pour un film donné
        en utilisant les informations récupérées via la méthode
        recuperer_streaming de l'objet Film.

        Args:
            film (Film): Le film pour lequel les plateformes de streaming
                         doivent être ajoutées.
        """
        try:
            streaming_info = film.recuperer_streaming()
            for plateforme in streaming_info:
                id_plateforme = plateforme["id"]
                nom_plateforme = plateforme["name"]
                success_ajout_plateforme = (
                    self.mettre_a_jour_plateforme(
                        nom_plateforme, id_plateforme
                    )
                )

                if success_ajout_plateforme:
                    logging.info(
                        f"La plateforme {nom_plateforme} a été ajoutée."
                    )
                else:
                    logging.info(
                        f"La plateforme {nom_plateforme} existe déjà."
                    )

                PlateformeDAO().ajouter_relation_film_plateforme(
                    film.id_film, id_plateforme
                )
        except Exception as e:
            print(f"Erreur pour le film {film.id_film}: {e}")
