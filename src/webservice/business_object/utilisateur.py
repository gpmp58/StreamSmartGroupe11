import re


class Utilisateur:
    """
    Classe représentant un Utilisateur

    Attributs
    ----------
    id_utilisateur : int
        identifiant
    nom : str
        nom de l'utilisateur
    prénom : str
        prénom de l'utilisateur
    adresse_mail : str
        adresse mail de l'utilisateur
    mdp : str
        le mot de passe de l'utilisateur
    langue :str
        la langue de l'utilisateur
    sel : str
        le sel utilisé pour hacher le mot de passe
    """

    def __init__(
        self,
        nom: str,
        prenom: str,
        pseudo: str,
        adresse_mail: str,
        mdp: str,
        id_utilisateur: int,
        langue: str = "français",
        sel: str = None,
    ):
        """
        Initialise un objet Utilisateur avec les attributs spécifiés.

        Args:
            nom (str) : Le nom renseigné par l'utilisateur.
            prenom (str) : Le prenom renseigné par l'utilisateur.
            pseudo (str) : Le pseudo renseigné par l'utilisateur.
            adresse_mail (str) : L'adresse mail renseignée par l'utilisateur.
            langue (str) : La langue de renseignée par l'utilisateur, si différente de celle par défaut.
            mdp (str) : Le mot de passe renseignée par l'utilisateur.
            id_utilisateur (int) : l'identifiant de l'utilisateur.
            sel (str) : Le sel utilisé pour hacher le mot de passe (optionnel).

        Raises:
            Exception: Si le nom n'est pas une chaîne de caractères.
            Exception: Si le prenom n'est pas une chaîne de caractères.
            Exception: Si le pseudo n'est pas une chaîne de caractères ou si il contient des caractères spéciaux.
            Exception: Si l'adresse mail n'est pas une chaîne de caractères ou si elle n'est pas valide.
            Exception: Si la langue n'est pas une chaîne de caractères.
            Exception: Si le mot de passe n'est pas une chaîne de caractères.
            Exception: Si id_utilisateur n'est pas un entier.
            Exception: Si le sel n'est pas une chaîne de caractères.
        """

        if not isinstance(nom, str):
            raise Exception("Le nom n'est pas une chaîne de caractères.")
        if not isinstance(prenom, str):
            raise Exception("Le prenom n'est pas une chaîne de caractères.")
        if not isinstance(pseudo, str):
            raise Exception("Le pseudo n'est pas une chaîne de caractères.")
        for caractere in pseudo:
            if not (caractere.isalnum() or caractere ==
                    "_" or caractere == "."):
                raise Exception(
                    "Il y a des caratères non autorisés dans le pseudo")
        if not isinstance(adresse_mail, str):
            raise Exception(
                "L'adresse mail n'est pas une chaîne de caractères.")
        if not self.is_valid_email(adresse_mail):
            raise Exception("L'adresse mail n'est pas valide.")
        if not isinstance(langue, str):
            raise Exception("La langue n'est pas une chaîne de caractères.")
        if not isinstance(mdp, str):
            raise Exception(
                "Le mot de passe n'est pas une chaîne de caractères.")
        if not isinstance(id_utilisateur, int):
            raise Exception(
                "L'identifiant de l'utilisateur n'est pas un entier.")
        if sel is not None and not isinstance(sel, str):
            raise Exception("Le sel n'est pas une chaîne de caractères.")

        self.id_utilisateur = id_utilisateur
        self.nom = nom
        self.prenom = prenom
        self.pseudo = pseudo
        self.adresse_mail = adresse_mail
        self.mdp = mdp
        self.langue = langue
        self.sel = sel

    @staticmethod
    def is_valid_email(adresse_mail: str):
        """
        Vérifie si l'adresse email fournie est valide selon une expression régulière : une partie avant le "@" suivie d'une partie après le "@", et une extension après un "."

        Args :
            adresse_mail (str) : L'adresse email de l'utilisateur à valider.

        Returns :
            bool : Retourne True si l'adresse email respecte le format de base, sinon False.
        """
        return re.match(r"[^@]+@[^@]+\.[^@]+", adresse_mail) is not None

    def message(self):
        """
        Permet d'afficher un message de bienvenue

        Returns:
            str : Message de bienvenue.
        """
        return f"Bienvenue {self.prenom} sur notre application !"

    def info_utilisateur(self) -> dict:
        """
        Retourne les attributs de l'utilisateur sous forme de dictionnaire

        Returns :
            dict : Attributs de l'utilisateur
        """
        return {
            "Nom": self.nom,
            "Prénom": self.prenom,
            "Pseudo": self.pseudo,
            "Adresse mail": self.adresse_mail,
            "Langue": self.langue,
            "id_utilisateur": self.id_utilisateur,
            "sel": self.sel,  # Ajout du sel dans le dictionnaire des informations utilisateur
        }

    def get_nom(self):
        """
        Retourne le nom de l'utilisateur.

        Returns:
            str : Nom de l'utilisateur.
        """
        return self.nom

    def get_prenom(self):
        """
        Retourne le prénom de l'utilisateur.

        Returns:
            str : Prenom de l'utilisateur.
        """
        return self.prenom

    def get_pseudo(self):
        """
        Retourne le psuedo de l'utilisateur.

        Returns:
            str : Pseudo de l'utilisateur.
        """
        return self.pseudo

    def get_adresse_mail(self):
        """
        Retourne l'adresse mail de l'utilisateur.

        Returns:
            str : Adresse mail de l'utilisateur.
        """
        return self.adresse_mail

    def get_langue(self):
        """
        Retourne la langue de l'utilisateur (bien que considérée comme étant le français pour tous les utilisateurs).

        Returns:
            str : Langue de l'utilisateur.
        """
        return self.langue

    def get_id_utilisateur(self):
        """
        Retourne l'identifiant de l'utilisateur.

        Returns:
            int : Identifiant de l'utilisateur.
        """
        return self.id_utilisateur

    def get_sel(self):
        """
        Retourne le sel pour l'utilisateur.

        Returns:
            str : Sel pour l'utilisateur.
        """
        return self.sel  # Ajout d'un getter pour récupérer le sel
