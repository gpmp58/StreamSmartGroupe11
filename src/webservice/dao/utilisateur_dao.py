from src.webservice.business_object.utilisateur import Utilisateur
from src.webservice.dao.db_connection import DBConnection
from src.webservice.utils.securite import verify_mdp


class UtilisateurDAO:
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
                # Ajout du champ `sel` dans la requête d'insertion
                cursor.execute(
                    "INSERT INTO projet11.utilisateur (nom, prenom, adresse_mail, mdp, pseudo, langue, sel) VALUES "
                    "(%(nom)s, %(prenom)s, %(adresse_mail)s, %(mdp)s, %(pseudo)s, %(langue)s, %(sel)s) "
                    "RETURNING id_utilisateur;",  # `RETURNING` pour récupérer l'id_utilisateur après création
                    {
                        "nom": utilisateur.nom,
                        "prenom": utilisateur.prenom,
                        "adresse_mail": utilisateur.adresse_mail,
                        "mdp": utilisateur.mdp,  # mdp est maintenant un mot de passe haché
                        "pseudo": utilisateur.pseudo,
                        "langue": utilisateur.langue,
                        "sel": utilisateur.sel,  # Le sel est ajouté pour être stocké dans la base de données
                    },
                )
                res = cursor.fetchone()

        created = False
        if res:
            utilisateur.id_utilisateur = res["id_utilisateur"]  # Mise à jour de l'id_utilisateur après création
            created = True

        return created


    def trouver_par_id(self, id_utilisateur) -> Utilisateur:
        """Trouver un utilisateur grâce à son id

        Parameters
        ----------
        id : int
            id que l'on souhaite trouver

        Returns
        -------
        utilisateur : Utilisateur
            renvoie l'utilisateur que l'on cherche par son id
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                # Requête de sélection pour récupérer un utilisateur avec son id
                cursor.execute(
                    "SELECT * FROM projet11.utilisateur WHERE id_utilisateur = %(id_utilisateur)s;",
                    {"id_utilisateur": id},
                )
                res = cursor.fetchone()

        utilisateur = None
        if res:
            # Création de l'objet Utilisateur avec les informations, y compris le sel récupéré
            utilisateur = Utilisateur(
                pseudo=res["pseudo"],
                mdp=res["mdp"],  # Mot de passe haché
                nom=res["nom"],
                prénom=res["prénom"],
                adresse_mail=res["adresse_mail"],
                langue=res["langue"],
                sel=res["sel"],  # Récupération du sel associé à l'utilisateur
                id_utilisateur=res["id_utilisateur"],
            )

        return utilisateur

    def modifier_DAO(self, utilisateur) -> bool:
        """Modification d'un utilisateur dans la base de données

        Parameters
        ----------
        utilisateur : Utilisateur

        Returns
        -------
        modified : bool
            True si la modification est un succès
            False sinon
        """
        res = None

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                # Mise à jour de l'utilisateur, ajout du champ `sel` si besoin d'être mis à jour
                cursor.execute(
                    "UPDATE projet11.utilisateur "
                    "SET mdp = %(mdp)s, nom = %(nom)s, prénom = %(prénom)s, adresse_mail = %(adresse_mail)s, sel = %(sel)s "
                    "WHERE pseudo = %(pseudo)s;",  # `sel` est ajouté pour s'assurer qu'il est aussi mis à jour si nécessaire
                    {
                        "mdp": utilisateur.mdp,  # Nouveau mot de passe haché
                        "nom": utilisateur.nom,
                        "prénom": utilisateur.prénom,
                        "adresse_mail": utilisateur.adresse_mail,
                        "pseudo": utilisateur.pseudo,
                        "sel": utilisateur.sel,  # Mise à jour du sel associé
                    },
                )
                res = cursor.rowcount

        return res == 1

    def supprimer_compte_DAO(self, utilisateur) -> bool:
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
                # Suppression de l'utilisateur par `id_utilisateur`
                cursor.execute(
                    "DELETE FROM projet11.utilisateur WHERE id_utilisateur = %(id_utilisateur)s",
                    {"id_utilisateur": utilisateur.id_utilisateur},
                )
                res = cursor.rowcount

        return res > 0

    def se_connecter_DAO(self, pseudo: str) -> Utilisateur:
        """Récupérer l'utilisateur par pseudo pour vérifier le mot de passe

        Parameters
        ----------
        pseudo : str
            pseudo de l'utilisateur

        Returns
        -------
        utilisateur : Utilisateur
            renvoie l'utilisateur que l'on cherche
        """
        res = None
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                # Requête SQL pour récupérer toutes les informations de l'utilisateur
                cursor.execute(
                    "SELECT * FROM projet11.utilisateur WHERE pseudo = %(pseudo)s;",
                    {"pseudo": pseudo},
                )
                res = cursor.fetchone()

        utilisateur = None
        if res:
            return res
        else:
            raise ValueError("Pseudo Introuvable")



    def trouver_watchlist_correspondante(self, utilisateur) -> list:
        """
        Cette méthode cherche la watchlist correspondant à un utilisateur.
        Si aucune watchlist n'est trouvée, elle retourne un message invitant à en créer une.
        """
        res = None
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                # Récupération des watchlists pour un utilisateur donné par `id_utilisateur`
                cursor.execute(
                    "SELECT w.id_watchlist, w.nom_watchlist "
                    "FROM utilisateur AS u "
                    "JOIN watchlist AS w "
                    "ON u.id_utilisateur = w.id_utilisateur "
                    "WHERE u.id_utilisateur = %(id_utilisateur)s",
                    {"id_utilisateur": utilisateur.id_utilisateur},
                )
                res = (
                    cursor.fetchall()
                )  # Utiliser `fetchall` pour obtenir toutes les watchlists

        if res:
            # Construire une liste de dictionnaires pour chaque watchlist
            return [
                {
                    "id_watchlist": row["id_watchlist"],
                    "nom_watchlist": row["nom_watchlist"],
                }
                for row in res
            ]
        else:
            return []
