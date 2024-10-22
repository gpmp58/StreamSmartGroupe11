from src.webservice.business_object.plateforme import PlateformeStreaming

class service_plateforme():
    def mettre_a_jour_plateforme(self, id_plateforme, nom_plateforme):
        nouvelle_plateforme = PlateformeStreaming(id_plateforme, nom_plateforme)
        return PlateformeDAO().ajouter_plateforme(nouvelle_plateforme)
