from business_object.utilisateur import Utilisateur
from dao.db_connection import DBConnection

class UtilisateurDAO():
    """Classe contenant les méthodes pour accéder aux utilisateurs de la base des données"""

    
    def creer_compte_DAO(self, utilisateur) -> bool:
        """Creation d'un joueur dans la base de données

        Parameters
        ----------
        utilisateur : Utilisateur

        Returns
        -------
        created : bool
            True si la création est un succès
            False sinon
        """

        res = None

        
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO utilisateur(nom, prénom, adresse_mail, mdp) VALUES "
                    "(%(pseudo)s,%(nom)s, %(prénom)s, %(adresse_mail)s, %(pseudo)s, %(mdp)s,%(langue)s) "
                    "  RETURNING id_utilisateur;",
                    {
                        "nom": utilisateur.nom,
                        "prénom": utilisateur.prénom,
                        "adresse_mail": utilisateur.adresse_mail,
                        "mdp": utilisateur.mdp,
                        "pseudo" : utilisateur.pseudo,
                        "langue" : utilisateur.langue,
                    },
                )
                res = cursor.fetchone()

        created = False
        if res:
            utilisateur.id_utilisateur= res["id_utilisateur"]
            created = True

        return created

    
    def trouver_par_id(self, id) -> Utilisateur:
        """trouver un utilisateur grace à son pseudo

        Parameters
        ----------
        pseudo : str
            pseudo de l'utilisateur id que l'on souhaite trouver

        Returns
        -------
        utilisateur : Utilisateur
            renvoie l'utilisateur que l'on cherche par pseudo
        """
        
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT *                           "
                    "  FROM utilisateur                      "
                    " WHERE id_utilisateur = %(id_utilisateur)s;  ",
                    {"id_utilisateur": id},
                )
                res = cursor.fetchone()
        utilisateur = None
        if res : 
            utilisateur = Utilisateur(
                pseudo=res["pseudo"],
                mdp=res["mdp"],
                nom=res["nom"],
                prénom=res["prénom"],
                adresse_mail=res["adresse_mail"],
                langue=res["langue"],
                id_utilisateur=res["id_utilisateur"]
            )


        return utilisateur

    
    def modifier_DAO(self, utilisateur) -> bool:
        """Modification d'un utilisateur dans la base de données

        Parameters
        ----------
        utilisateur : Utilisateur

        Returns
        -------
        created : bool
            True si la modification est un succès
            False sinon
        """

        res = None

       
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE utilisateur                                      "
                    "   SET mdp         = %(mdp)s,                      "
                    "       nom         = %(nom)s,                      "
                    "       prénom      = %(prénom)s,                     "
                    "       adresse_mail = %(adresse_mail)s               "
                    " WHERE pseudo = %(pseudo)s;                  ",
                    {
                        "mdp": utilisateur.mdp,
                        "nom": utilisateur.nom,
                        "prénom": utilisateur.prénom,
                        "adresse_mail": utilisateur.adresse_mail,
                        "pseudo": utilisateur.pseudo,
                    },
                )
                res = cursor.rowcount

        return res == 1

    
    def supprimer_compte_DAO(self, utilsateur) -> bool:
        """Suppression d'un utilisateur dans la base de données

        Parameters
        ----------
        utilisateur : Utilisateur
            utilisateur à supprimer de la base de données

        Returns
        -------
            True si l'utilisateur a bien été supprimé
        """

        
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM utilisateur             "
                    " WHERE id_utilisateur = %(id_utilisateur)s      ",
                    {"id_utilisateur": utilisateur.id_utilisateur},
                )
                res = cursor.rowcount

        return res > 0

    def se_connecter_DAO(self, pseudo, mdp) -> Utilisateur:
        """se connecter grâce à son pseudo et son mot de passe

        Parameters
        ----------
        pseudo : str
            pseudo d'utilisateur que l'on souhaite trouver
        mdp : str
            mot de passe d'utilisateur

        Returns
        -------
        utilisateur : Utlisateur
            renvoie l'utilisateur que l'on cherche
        """
        res = None
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT *                           "
                    "  FROM utilisateur                 "
                    " WHERE id_utilisateur = %(id_utilisateur)s         "
                    "   AND mdp = %(mdp)s;              ",
                    {"id_utilisateur": id_utilisateur, "mdp": mdp},
                )
                res = cursor.fetchone()


        utilisateur = None

        if res:
            utilisateur = Utilisateur(
                pseudo=res["pseudo"],
                mdp=res["mdp"],
                nom=res["nom"],
                prénom=res["prénom"],
                adresse_mail=res["adresse_mail"],
                langue=res["langue"],
                id_utilisateur=res["id_utilisateur"]
            )

        return utilisateur
    
def trouver_watchlist_correspondante(self, utilisateur) -> list:
    """
    Cette méthode cherche la watchlist correspondant à un utilisateur.
    Si aucune watchlist n'est trouvée, elle retourne un message invitant à en créer une.
    """
    res = None
    with DBConnection().connection as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT w.id_watchlist, w.nom_watchlist "
                "FROM utilisateur AS u "
                "JOIN watchlist AS w "
                "ON u.id_utilisateur = w.id_utilisateur "
                "WHERE u.id_utilisateur = %(id_utilisateur)s",  
                {"id_utilisateur": utilisateur.id_utilisateur},
            )
            res = cursor.fetchone()
    
    if res:
        return [{"id_watchlist": row["id_watchlist"], "nom_watchlist": row["nom_watchlist"]} for row in res]
    else:
        return []