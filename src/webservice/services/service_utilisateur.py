from dao.utilisateur_dao import UtilisateurDAO
from utils.log_decorator import log
from utils.securite import hash_password
from business_object.utilisateur import Utilisateur

class UtilisateurService:
    """
    La classe UtilisateurService fournit des méthodes de haut niveau pour la gestion des utilisateurs,
    telles que la création de comptes, la suppression de comptes, la connexion, la déconnexion, et l'affichage
    des informations d'un utilisateur. Elle s'appuie sur UtilisateurDAO pour interagir avec la base de données.

    Attributs :
    -----------
    utilisateur_dao : UtilisateurDAO
        Instance de la classe UtilisateurDAO pour effectuer des opérations CRUD sur la base de données.
    """
    
    def __init__(self, utilisateur_dao: UtilisateurDAO):
        """
        Initialise un nouvel objet UtilisateurService avec un DAO utilisateur donné.

        Paramètres :
        ------------
        utilisateur_dao : UtilisateurDAO
            Une instance de la classe UtilisateurDAO utilisée pour interagir avec la base de données.
        """
        self.utilisateur_dao = utilisateur_dao

    
    def creer_compte(self, nom: str, prenom: str, adresse_mail: str, pseudo: str, mdp: str):
        """
        Crée un nouvel utilisateur dans la base de données.

        Paramètres :
        ------------
        nom : str
            Le nom de l'utilisateur.
        prenom : str
            Le prénom de l'utilisateur.
        adresse_mail : str
            L'adresse e-mail de l'utilisateur.
        pseudo : str
            Le pseudo unique de l'utilisateur.
        mdp : str
            Le mot de passe de l'utilisateur qui sera haché pour la sécurité.

        Exceptions :
        ------------
        ValueError
            Si l'utilisateur existe déjà (vérification à implémenter au niveau du DAO).
        """
        
        # Créer un objet Utilisateur
        utilisateur = Utilisateur(nom=nom, prenom=prenom, adresse_mail=adresse_mail, pseudo=pseudo, mdp=mdp)

        # Créer l'utilisateur dans la base de données
        if not self.utilisateur_dao.creer_compte_DAO(utilisateur):
            raise ValueError("Erreur lors de la création du compte. Pseudo peut-être déjà utilisé.")

    
    def supprimer_compte(self, pseudo: str):
        """
        Supprime un compte utilisateur basé sur le pseudo.

        Paramètres :
        ------------
        pseudo : str
            Le pseudo de l'utilisateur à supprimer.

        Exceptions :
        ------------
        ValueError
            Si l'utilisateur n'est pas trouvé dans la base de données.
        """
        # Vérifier si l'utilisateur existe avant de le supprimer
        utilisateur = self.utilisateur_dao.trouver_par_pseudo(pseudo)
        if utilisateur:
            self.utilisateur_dao.supprimer_compte_DAO(utilisateur)
        else:
            raise ValueError("Utilisateur introuvable.")

    
    def se_connecter(self, pseudo: str, mdp: str):
        """
        Permet à un utilisateur de se connecter en vérifiant son pseudo et son mot de passe.

        Paramètres :
        ------------
        pseudo : str
            Le pseudo de l'utilisateur.
        mdp : str
            Le mot de passe de l'utilisateur.

        Exceptions :
        ------------
        ValueError
            Si les informations de connexion sont incorrectes.
        """

        # Trouver l'utilisateur dans la base de données via le pseudo & mdp
        utilisateur = self.utilisateur_dao.se_connecter_DAO(pseudo, mdp)
        #Cas où le mdp/pseudo sont incorrects , l'utilisateur n'est pas trouvé -> la fct renvoie None
        if utilisateur==None:
            raise ValueError("Pseudo ou mdp incorrect")
        #Cas de succès: on doit le rediriger vers la page d'acceuil avec message de bienvenue
        else:
            return f"Bienvenue {utilisateur.pseudo} sur notre application"

    
    def se_deconnecter(self):
        """
        Déconnecte l'utilisateur actuellement connecté.
        Cette méthode peut être utilisée pour mettre fin à une session utilisateur active.

        Remarque :
        ------------
        Le mécanisme de session n'est pas directement implémenté ici, il dépend d'autres couches
        de l'application (par exemple, une session Flask).
        """
        # Gérer la déconnexion --> renvoie vers une fausse page de déconnexion
        print("Déconnexion réussie")

    
    def afficher(self, pseudo: str):
        """
        Affiche les informations d'un utilisateur basé sur son pseudo.

        Paramètres :
        ------------
        pseudo : str
            Le pseudo de l'utilisateur dont on souhaite afficher les informations.

        Exceptions :
        ------------
        ValueError
            Si l'utilisateur n'est pas trouvé dans la base de données.
        """