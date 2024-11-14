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

    """def __init__(self, utilisateur: Utilisateur):
        Initialise un nouvel objet UtilisateurService avec un DAO utilisateur
        donné.

        Paramètres :
        ------------
        utilisateur : Utilisateur
            Une instance de la classe Utilisateur utilisée pour interagir
            avec la base de données.
        
        self.utilisateur = utilisateur"""
        

    def creer_compte(self, nom: str, prenom: str, pseudo: str, adresse_mail: str, mdp: str, langue: str = "français") -> Utilisateur:
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
            Si le pseudo est déjà utilisé ou si une erreur survient lors de la création.
        """
        try:
            # Vérifier si le pseudo existe déjà
            if self.verifier_pseudo(pseudo):
                raise ValueError("Le pseudo est déjà utilisé. Veuillez en choisir un autre.")

            # Hacher le mot de passe avec un sel aléatoire
            hashed_mdp, sel = hash_mdp(mdp)

            # Appeler le DAO pour créer un utilisateur en base de données
            id_utilisateur = UtilisateurDAO().creer_compte_DAO(
                nom=nom,
                prenom=prenom,
                pseudo=pseudo,
                adresse_mail=adresse_mail,
                mdp=hashed_mdp,
                langue=langue,
                sel=sel
            )

            # Vérifier le succès de la création
            if id_utilisateur is None:
                raise ValueError("Erreur lors de la création du compte.")

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
            # Lever l'exception au lieu de renvoyer un dictionnaire pour permettre une gestion des erreurs cohérente
            raise ValueError(f"Erreur lors de la création de l'utilisateur : {e}")

    def supprimer_compte(self, id_utilisateur: int):
        """
        Supprime un compte utilisateur basé sur l'id de l'utilisateur.

        Paramètres :
        ------------
        id_utilisateur : int
            L'identifiant de l'utilisateur à supprimer.

        Exceptions :
        ------------
        ValueError
            Si l'utilisateur n'est pas trouvé dans la base de données.
        """
        try:
            # Utiliser le DAO pour supprimer l'utilisateur
            succes = UtilisateurDAO().supprimer_compte_DAO(id_utilisateur)
            if not succes:
                raise ValueError("Utilisateur introuvable ou suppression échouée.")
            print(f"Compte avec l'id '{id_utilisateur}' supprimé avec succès.")
        except Exception as e:
            raise ValueError(f"Erreur lors de la suppression de l'utilisateur : {e}")

    def se_connecter(self, pseudo: str, mdp: str):
        """
        Permet à un utilisateur de se connecter en vérifiant son pseudo et son
        mot de passe.

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
        try:
            # Récupérer l'utilisateur par pseudo
            utilisateur_connecte = UtilisateurDAO().se_connecter_DAO(pseudo)
            mdp_stocke = utilisateur_connecte["mdp"]  # Mot de passe haché stocké dans la db
            sel = utilisateur_connecte["sel"]  # Le sel utilisé pour hacher le mot de passe

            # Hacher le mot de passe fourni par l'utilisateur avec le sel récupéré
            hashed_mdp, _ = hash_mdp(mdp, sel)

            # Vérifier si le mot de passe haché correspond à celui stocké
            if mdp_stocke != hashed_mdp:
                raise ValueError("Pseudo ou mot de passe incorrect.")

            return f"Bienvenue {pseudo} sur notre application"
        except Exception as e:
            raise ValueError(f"Erreur lors de la connexion de l'utilisateur : {e}")

    def se_deconnecter(self):
        """
        Déconnecte l'utilisateur actuellement connecté.
        Cette méthode peut être utilisée pour mettre fin à une session
        utilisateur active.
        """
        pass

    def afficher(self, id_utilisateur: int):
        """
        Affiche les informations d'un utilisateur basé sur son id.

        Paramètres :
        ------------
        id_utilisateur : int
            L'identifiant de l'utilisateur dont on souhaite afficher les
            informations.

        Returns:
        --------
        dict
            Les informations de l'utilisateur.
        
        Exceptions :
        ------------
        ValueError
            Si l'utilisateur n'est pas trouvé dans la base de données.
        """
        try:
            utilisateur = UtilisateurDAO().trouver_par_id(id_utilisateur)

            if utilisateur:
                utilisateur_info = {
                    "Nom": utilisateur.nom,
                    "Prénom": utilisateur.prenom,
                    "Pseudo": utilisateur.pseudo,
                    "Adresse mail": utilisateur.adresse_mail,
                    "Langue": utilisateur.langue
                }
                return utilisateur_info
            else:
                raise ValueError("Utilisateur introuvable.")
        except Exception as e:
            raise ValueError(f"Erreur lors de l'affichage des informations de l'utilisateur : {e}")

    def verifier_pseudo(self, pseudo: str) -> bool:
        """
        Vérifie si un pseudo existe déjà dans la base de données.

        Paramètres :
        ------------
        pseudo : str
            Le pseudo à vérifier.

        Returns :
        ---------
        bool
            True si le pseudo existe, False sinon.

        Exceptions :
        ------------
        ValueError
            Si une erreur survient lors de la vérification.
        """
        try:
            existe = UtilisateurDAO().existe_pseudo_DAO(pseudo)
            return existe
        except Exception as e:
            raise ValueError(f"Erreur lors de la vérification du pseudo : {e}")
