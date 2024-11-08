from src.webservice.business_object.plateforme import PlateformeStreaming
from src.webservice.dao.plateforme_dao import PlateformeDAO


class service_plateforme:
    """
    Service de gestion des plateformes de streaming.Cette classe fournit une méthode pour mettre à jour une plateforme dans la base de données.
    """
    def mettre_a_jour_plateforme(self, id_plateforme, nom_plateforme):
        """
        Met à jour ou ajoute une nouvelle plateforme de streaming dans la base de données.

        Args:
            id_plateforme (int) : L'identifiant de la plateforme de streaming.
            nom_plateforme (str) : Le nom de la plateforme de streaming.

        Returns:
            bool : True si la plateforme a été ajoutée avec succès, False si la plateforme existe déjà.
        """
        nouvelle_plateforme = PlateformeStreaming(id_plateforme, nom_plateforme)
        return PlateformeDAO().ajouter_plateforme(nouvelle_plateforme)
