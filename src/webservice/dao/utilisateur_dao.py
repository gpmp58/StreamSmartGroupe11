
from dao.db_connection import DBConnection

from business_object.utilisateur import Utilisateur


class utilisateurDao():
    """Classe contenant les méthodes pour accéder aux utilisateurs de la base des données"""

    
    def creer(self, utilisateur) -> bool:
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
                    "(%(nom)s, %(prénom)s, %(adresse_mail)s, %(pseudo)s, %(mdp)s) "
                    "  RETURNING pseudo;",
                    {
                        "nom": utilisateur.nom,
                        "prénom": utilisateur.prénom,
                        "adresse_mail": utilisateur.adresse_mail,
                        "mdp": utilisateur.mdp,
                    },
                )
                res = cursor.fetchone()

        created = False
        if res:
            pseudo = res["pseudo"]
            created = True

        return created

    
    def trouver_par_pseudo(self, pseudo) -> Utilisateur:
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
                    " WHERE pseudo = %(pseudo)s;  ",
                    {"pseudo": pseudo},
                )
                res = cursor.fetchone()
        utilisateur = None
        if res:
            utilisateur = Utilisateur(
                pseudo=res["pseudo"],
                nom=res["nom"],
                prénom=res["prénom"],
                adresse_mail=res["adresse_mail"],
            )

        return joueur

    
    def modifier(self, utilisateur) -> bool:
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

    
    def supprimer(self, utilsateur) -> bool:
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
                    " WHERE pseudo = %(pseudo)s      ",
                    {"pseudo": Utilisateur.pseudo},
                )
                res = cursor.rowcount

        return res > 0

    def se_connecter(self, pseudo, mdp) -> Utilisateur:
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
                    " WHERE pseudo = %(pseudo)s         "
                    "   AND mdp = %(mdp)s;              ",
                    {"pseudo": pseudo, "mdp": mdp},
                )
                res = cursor.fetchone()


        utilisateur = None

        if res:
            utilisateur = Utilisateur(
                pseudo=res["pseudo"],
                mdp=res["mdp"],
                nom=res["nom"],
                prénom=res["prénom"],
                adresse_mail=res["adresse_mail"]
            )

        return utilisateur
    
    def trouver_watchlist_correspondante(self,utilisateur) -> int:
        """
        description de la commande 
        """
        res = None
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id_watchlist                "
                    "FROM utilisateur as u               "
                    "JOIN utilisateur_watchlist as w"
                    "ON u.pseudo = w.pseudo"
                    "JOIN watchlist as wu"
                    "ON wu.id_watchlist = w.id_watchlist",
                    {"pseudo": utilisateur.pseudo},

                )
                res = cursor.fetchone()
        if res :
            return res[id_watchlist]
        else :
            return("C'est le temps de créer votre watchlist ! ")