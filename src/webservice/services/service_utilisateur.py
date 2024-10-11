from dao.utilisateur_dao import UtilisateurDAO
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

    def creer_compte(self, nom: str, prenom: str, pseudo: str, adresse_mail: str, mdp: str, langue: str = "français"):
        """
        Crée un nouvel utilisateur dans la base de données.

        Paramètres :
        ------------
        nom : str
            Le nom de l'utilisateur.
        prenom : str
            Le prénom de l'utilisateur.
        pseudo : str
            Le pseudo unique de l'utilisateur.
        adresse_mail : str
            L'adresse e-mail de l'utilisateur.
        mdp : str
            Le mot de passe de l'utilisateur.
        langue : str
            La langue de l'utilisateur, par défaut "français".

        Returns :
        ---------
        str
            Un message indiquant le succès de la création du compte.

        Exceptions :
        ------------
        ValueError
            Si l'utilisateur existe déjà (vérification à implémenter au niveau du DAO).
        dict
            Contient une clé "error" avec le message d'erreur si la création a échoué.
        """
        try:
            # Créer un objet Utilisateur
            nouvel_utilisateur = Utilisateur(nom=nom, prenom=prenom, pseudo=pseudo, adresse_mail=adresse_mail, mdp=mdp, langue=langue)

            # Créer l'utilisateur dans la base de données
            if not self.utilisateur_dao.creer_compte_DAO(nouvel_utilisateur):
                raise ValueError("Erreur lors de la création du compte. Le pseudo est peut-être déjà utilisé.")

            # Retourner l'utilisateur créé en cas de succès
            return f"Nouveau compte créé : {nouvel_utilisateur}"

        except Exception as e:
            # Retourner un dictionnaire contenant l'erreur
            return {"error": str(e)}

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
        utilisateur = self.utilisateur_dao.trouver_par_pseudo(pseudo)
        if utilisateur:
            self.utilisateur_dao.supprimer_compte_DAO(utilisateur)
            print(f"Compte avec le pseudo '{pseudo}' supprimé avec succès.")
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

        Returns :
        ---------
        str
            Un message de bienvenue en cas de succès.

        Exceptions :
        ------------
        ValueError
            Si les informations de connexion sont incorrectes.
        """
        # Trouver l'utilisateur dans la base de données via le pseudo et le mot de passe
        utilisateur_connexion = self.utilisateur_dao.se_connecter_DAO(pseudo, mdp)
        
        if utilisateur_connexion is None:
            raise ValueError("Pseudo ou mot de passe incorrect.")
        else:
            return f"Bienvenue {utilisateur.pseudo} sur notre application"

    def se_deconnecter(self):
        """
        Déconnecte l'utilisateur actuellement connecté.
        Cette méthode peut être utilisée pour mettre fin à une session utilisateur active.

        Remarque :
        ------------
        Le mécanisme de session n'est pas directement implémenté ici et dépend d'autres couches
        de l'application (par exemple, une session Flask).
        """
        print("Déconnexion réussie.")

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
        utilisateur = self.utilisateur_dao.trouver_par_pseudo(pseudo)

        if utilisateur:
            print(f"Nom: {utilisateur.nom}, Prénom: {utilisateur.prenom}, "
                  f"Email: {utilisateur.adresse_mail}, Langue: {utilisateur.langue}")
        else:
            raise ValueError("Utilisateur introuvable.")
