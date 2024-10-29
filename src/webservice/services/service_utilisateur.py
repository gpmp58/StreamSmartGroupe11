from src.webservice.business_object.utilisateur import Utilisateur
from src.webservice.utils.securite import hash_mdp, verify_mdp
from src.webservice.dao.utilisateur_dao import UtilisateurDAO


class UtilisateurService:
    """
    La classe UtilisateurService fournit des méthodes de haut niveau pour la
    gestion des utilisateurs, telles que la création de comptes, la suppression
    de comptes, la connexion, la déconnexion, et l'affichage des informations
    d'un utilisateur. Elle s'appuie sur UtilisateurDAO pour interagir avec la
    base de données.
    """

    def __init__(self, utilisateur: Utilisateur):
        """
        Initialise un nouvel objet UtilisateurService avec un DAO utilisateur
        donné.

        Paramètres :
        ------------
        utilisateur : Utilisateur
            Une instance de la classe Utilisateur utilisée pour interagir
            avec la base de données.
        """
        self.utilisateur = utilisateur

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
        Utilisateur
            Retourne l'utilisateur créé en cas de succès.

        Exceptions :
        ------------
        ValueError
            Si l'utilisateur existe déjà (vérification à implémenter au niveau
            du DAO).
        """
        try:
            # Hacher le mot de passe avec un sel aléatoire
            hashed_mdp, sel = hash_mdp(mdp)

            # Appeler le DAO pour créer un utilisateur en base de données
            # creer_compte_DAO envoie l'id utilisateur ou renvoie False en cas d'échec
            id_utilisateur = self.utilisateur.creer_compte_DAO(
                nom=nom,
                prenom=prenom,
                pseudo=pseudo,
                adresse_mail=adresse_mail,
                mdp=hashed_mdp,
                langue=langue,
                sel=sel
            )

            # Vérifier le succès de la création
            if id_utilisateur is False:
                return {"error": "Erreur lors de la création du compte. Le pseudo est peut-être déjà utilisé."}
            
            # Si l'id_utilisateur n'est pas un entier, lever une erreur
            if not isinstance(id_utilisateur, int):
                raise ValueError("id_utilisateur n'est pas un entier.")

            # Créer l'objet Utilisateur avec les informations de l'utilisateur
            nouvel_utilisateur = Utilisateur(
                id_utilisateur=id_utilisateur,
                nom=nom,
                prenom=prenom,
                pseudo=pseudo,
                adresse_mail=adresse_mail,
                mdp=hashed_mdp,
                langue=langue,
                sel=sel
            )

            # Retourner l'utilisateur créé en cas de succès
            return nouvel_utilisateur

        except Exception as e:
            # Retourner un dictionnaire contenant l'erreur
            return {"error": str(e)}



    def supprimer_compte(self, id_utilisateur: str):
        """
        Supprime un compte utilisateur basé sur l'id de l'utilisateur.

        Paramètres :
        ------------
        id_utilisateur : str
            L'identifiant de l'utilisateur à supprimer.

        Exceptions :
        ------------
        ValueError
            Si l'utilisateur n'est pas trouvé dans la base de données.
        """
        utilisateur = self.utilisateur.trouver_par_id(id_utilisateur)
        if utilisateur:
            self.utilisateur.supprimer_compte_DAO(utilisateur)
            print(f"Compte avec l'id '{id_utilisateur}' supprimé avec succès.")
        else:
            raise ValueError("Utilisateur introuvable.")

    def se_connecter(self, pseudo: str, mdp: str):
        """
        Permet à un utilisateur de se connecter en vérifiant son pseudo et son
        mot de passe.

        Paramètres :
        ------------
        id_utilisateur : str
            L'id de l'utilisateur.
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
        utilisateur_connecte=UtilisateurDAO().se_connecter_DAO(pseudo)
        mdp_stocke=utilisateur_connecte["mdp"]  # Mot de passe haché stocke dans la db
        sel=utilisateur_connecte["sel"]  # Le sel utilisé pour hacher le mot de passe

        # hacher le mdp
        hashed_mdp, _ = hash_mdp(mdp, sel)

        # Vérifier si le mot de passe haché correspond à celui stocké
        if mdp_stocke != hashed_mdp:
            raise ValueError("Pseudo ou mot de passe incorrect.")

        return f"Bienvenue {utilisateur_connexion.pseudo} sur notre application"


    def se_deconnecter(self):
        """
        Déconnecte l'utilisateur actuellement connecté.
        Cette méthode peut être utilisée pour mettre fin à une session
        utilisateur active.
        """
        pass

    def afficher(self, id_utilisateur):
        """
        Affiche les informations d'un utilisateur basé sur son id.

        Paramètres :
        ------------
        id_utilisateur : str
            L'identifiant de l'utilisateur dont on souhaite afficher les
            informations.

        Exceptions :
        ------------
        ValueError
            Si l'utilisateur n'est pas trouvé dans la base de données.
        """
        utilisateur = self.utilisateur.trouver_par_id(id_utilisateur)

        if utilisateur:
            print(
                f"Nom: {utilisateur.nom}, Prénom: {utilisateur.prenom}, "
                f"Email: {utilisateur.adresse_mail}, Langue: "
                f"{utilisateur.langue}"
            )
        else:
            raise ValueError("Utilisateur introuvable.")
