from src.webservice.business_object.utilisateur import Utilisateur
from src.webservice.dao.db_connection import DBConnection
from src.webservice.utils.securite import verify_mdp


class UtilisateurDAO:
    """
    Classe contenant les méthodes pour accéder aux utilisateurs de la base de données.
    """

    def creer_compte_DAO(self, nom: str, prenom: str, pseudo: str, adresse_mail: str, mdp: str, langue: str = "français", sel: str = None) -> int:
        """
        Création d'un utilisateur dans la base de données.
        
        Args:
            nom (str) : Le nom de l'utilisateur.
            prenom (str) : Le prénom de l'utilisateur.
            pseudo (str) : Le pseudo de l'utilisateur.
            adresse_mail (str) : L'adresse email de l'utilisateur.
            mdp (str) : Le mot de passe de l'utilisateur.
            langue (str) : La langue de l'utilisateur (par défaut "français").
            sel (str) : Le sel utilisé pour le hachage du mot de passe.

        Returns:

        id_utilisateur : int
            L'ID utilisateur créé.

        Raises:
            ValueError : Si l'insertion échoue.
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO projet11.utilisateur (nom, prenom, adresse_mail, mdp, pseudo, langue, sel)
                    VALUES (%(nom)s, %(prenom)s, %(adresse_mail)s, %(mdp)s, %(pseudo)s, %(langue)s, %(sel)s)
                    RETURNING id_utilisateur;
                    """,
                    {
                        "nom": nom,
                        "prenom": prenom,
                        "adresse_mail": adresse_mail,
                        "mdp": mdp,
                        "pseudo": pseudo,
                        "langue": langue,
                        "sel": sel
                    }
                )
                res = cursor.fetchone()
                if res:
                    return res["id_utilisateur"]
                else:
                    raise ValueError("Erreur lors de la création de l'utilisateur.")

    def trouver_par_id(self, id_utilisateur: int) -> Utilisateur:
        """
        Trouver un utilisateur grâce à son id.

        Parameters:
        -----------
        id_utilisateur : int
            L'ID de l'utilisateur.

        Returns:
        --------
        Utilisateur : Instance de la classe Utilisateur contenant les informations de l'utilisateur.
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM projet11.utilisateur WHERE id_utilisateur = %(id_utilisateur)s;",
                    {"id_utilisateur": id_utilisateur}
                )
                res = cursor.fetchone()

        if res:
            return Utilisateur(
                id_utilisateur=res["id_utilisateur"],
                nom=res["nom"],
                prenom=res["prenom"],
                pseudo=res["pseudo"],
                adresse_mail=res["adresse_mail"],
                mdp=res["mdp"],
                langue=res["langue"],
                sel=res["sel"]
            )
        else:
            raise ValueError("Utilisateur introuvable.")

    def se_connecter_DAO(self, pseudo: str) -> dict:
        """
        Récupérer un utilisateur par pseudo pour vérifier le mot de passe.

        Parameters:
        -----------
        pseudo : str
            Le pseudo de l'utilisateur.

        Returns:
        --------
        dict : Dictionnaire contenant les informations de l'utilisateur.
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM projet11.utilisateur WHERE pseudo = %(pseudo)s;",
                    {"pseudo": pseudo}
                )
                res = cursor.fetchone()

        if res:
            return {
                "id_utilisateur": res["id_utilisateur"],
                "nom": res["nom"],
                "prenom": res["prenom"],
                "pseudo": res["pseudo"],
                "adresse_mail": res["adresse_mail"],
                "mdp": res["mdp"],
                "langue": res["langue"],
                "sel": res["sel"]
            }
        else:
            raise ValueError("Pseudo ou mot de passe incorrect.")


    def supprimer_compte_DAO(self, id_utilisateur: int) -> bool:
        """
        Suppression d'un utilisateur dans la base de données.

        Parameters:
        ----------
        id_utilisateur : int
            L'ID de l'utilisateur à supprimer.

        Returns:
        --------
            bool : True si l'utilisateur a bien été supprimé.
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM projet11.utilisateur WHERE id_utilisateur = %(id_utilisateur)s",
                    {"id_utilisateur": id_utilisateur},
                )
                res = cursor.rowcount

        return res > 0

    def existe_pseudo_DAO(self, pseudo: str) -> bool:
        """
        Vérifie si un pseudo existe déjà dans la base de données.

        Parameters:
        -----------
        pseudo : str
            Le pseudo à vérifier.

        Returns:
        --------
        bool
            True si le pseudo existe, False sinon.
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT 1 FROM projet11.utilisateur
                    WHERE pseudo = %(pseudo)s
                    LIMIT 1;
                    """,
                    {"pseudo": pseudo}
                )
                res = cursor.fetchone()

        return res is not None

    def get_id_utilisateur_DAO(self, pseudo: str) -> dict:
        """
        Récupère l'ID d'un utilisateur à partir de son pseudo.

        Parameters:
        -----------
        pseudo : str
            Le pseudo de l'utilisateur.

        Returns:
        --------
        dict : Contient l'ID de l'utilisateur.

        Raises:
        -------
        ValueError : Si aucun utilisateur n'est trouvé avec ce pseudo.
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id_utilisateur
                    FROM projet11.utilisateur
                    WHERE pseudo = %(pseudo)s;
                    """,
                    {"pseudo": pseudo}
                )
                res = cursor.fetchone()

        if res:
            return {"id_utilisateur": res["id_utilisateur"]}
        else:
            raise ValueError(f"Utilisateur avec le pseudo '{pseudo}' introuvable.")

