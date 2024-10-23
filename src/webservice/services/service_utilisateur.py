from src.webservice.business_object.utilisateur import Utilisateur
from src.webservice.utils.securite import hash_mdp, verify_mdp


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

    def creer_compte(
        self,
        nom: str,
        prenom: str,
        pseudo: str,
        adresse_mail: str,
        mdp: str,
        langue: str = "français",
    ):
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

            # Créer un objet Utilisateur avec le mot de passe haché et le sel
            nouvel_utilisateur = Utilisateur(
                nom=nom,
                prenom=prenom,
                pseudo=pseudo,
                adresse_mail=adresse_mail,
                mdp=hashed_mdp,
                langue=langue,
            )
            # Ajouter le sel en tant qu'attribut à l'utilisateur
            nouvel_utilisateur.sel = sel

            # Créer l'utilisateur dans la base de données
            if not self.utilisateur.creer_compte_DAO(nouvel_utilisateur):
                raise ValueError(
                    "Erreur lors de la création du compte. "
                    "Le pseudo est peut-être déjà utilisé."
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

    def se_connecter(self, pseudo: str, hash_mdp(mdp)):
        """
        Permet à un utilisateur de se connecter en vérifiant son pseudo et son
        mot de passe.

        Parameters :
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
        # Utiliser la méthode du DAO pour tenter la connexion
        utilisateur_connexion = self.utilisateur.se_connecter_DAO(pseudo, hash_mdp(mdp))

        # Si l'utilisateur n'existe pas, lever une erreur
        if utilisateur_connexion is None:
            raise ValueError("Pseudo ou mot de passe incorrect.")

        # Retourner un message de bienvenue si la vérification est réussie
        return f"Bienvenue {utilisateur_connexion.pseudo} sur notre application"


    def se_deconnecter(self):
        """
        Déconnecte l'utilisateur actuellement connecté.
        Cette méthode peut être utilisée pour mettre fin à une session
        utilisateur active.
        """
        print("Déconnexion réussie.")

    def afficher(self, id_utilisateur: str):
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
