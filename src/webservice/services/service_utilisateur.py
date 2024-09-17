from tabulate import tabulate
"""
from utils.log_decorator import log
from utils.securite import hash_password
"""
from business_object.utilisateur import Utilisateur

#from dao.joueur_dao import JoueurDao


class UtilisateurService:
    """Classe contenant les méthodes de service des Utilisateurs"""

    @log
    def creer(self, nom, prenom, adresse_mail, mdp, langue) -> Utilisateur:
        """Création d'un joueur à partir de ses attributs"""

        nouvel_Utilisateur = Utilisateur(
            nom=nom,
            prenom=prenom,
            adresse_mail=adresse_mail,
            mdp=mdp,
            langue=langue,
        )
        
        return nouvel_Utilisateur

    @log
    def trouver_par_id(self, id_utilisateur) -> Utilisateur:
        """Trouver un Utilisateur à partir de son id"""
        pass

    @log
    def modifier(self, utilisateur) -> Utilisateur:
        """Modification d'un utilisateur"""
    #On utilisera une méthode du DAO pour modifier dans la DB
        pass

    @log
    def supprimer(self, utilisateur) -> bool:
        """Supprimer le compte d'un joueur"""
        pass


    @log
    def se_connecter(self, pseudo, mdp) -> Joueur:
        """Se connecter à partir de pseudo et mdp"""
        pass

    @log
    def mail_deja_utilise(self, adresse_mail) -> bool:
        """Vérifie si l'adresse mail est déjà utilisée
        Retourne True si l'adresse existe déjà en BDD"""
        pass

    @log
    def afficher_tous(self) -> str:
        """Afficher tous les utilisateurs
        Sortie : Une chaine de caractères mise sous forme de tableau
        """
        pass