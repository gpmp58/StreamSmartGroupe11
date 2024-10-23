from src.webservice.business_object.plateforme import PlateformeStreaming
from src.webservice.business_object.abonnement import Abonnement
from src.dao.abonnement_dao import AbonnementDao

class AbonnementService():

    def prix_abonnement(self, id_abonnement):
        abonnement = Abonnement(id_abonnement)
        prix = AbonnementDao().get_prix_DAO(abonnement)
        return prix

    def pub_abonnement(self, id_abonnement):
        abonnement = Abonnement(id_abonnement)
        pub = AbonnementDao().get_pub_DAO(abonnement)
        if pub :
            return f"Cet abonnement contient des pub !"
        else :
            return f"Cet abonnement ne contient pas des pub !"

    def qualite_abonnement(self, id_abonnement):
        abonnement = Abonnement(id_abonnement)
        qualite = AbonnementDao().get_qualite_DAO(abonnement)
        return qualite
    
    def recherche_abonnement(self, nom_plateforme, id_plateforme):
        plateforme = PlateformeStreaming(nom_plateforme, id_plateforme)
        abonnement_list = AbonnementDao().get_abonnement(plateforme)
        return abonnement_list

    
