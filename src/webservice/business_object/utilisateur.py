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
        """Constructeur avec validation basique"""
        """
        Initialise un objet Utilisateur avec les attributs spécifiés.

        Args:
            nom (str) : Le nom renseigné par l'utilisateur.
            prenom (str) : Le prenom renseigné par l'utilisateur.
            pseudo (str) : Le pseudo renseigné par l'utilisateur.
            adresse_mail (str) : L'adresse mail renseignée par l'utilisateur.
            langue (str) : La langue de renseignée par l'utilisateur, si différente de celle par défaut.
            mdp (str) : Le mot de passe renseignée par l'utilisateur.
            id_utilisateur (int) : id_utilisateur.
            sel (str) : Le sel utilisé pour hacher le mot de passe (optionnel).

        Raises:
            Exception: Si le nom n'est pas une chaîne de caractères.
            Exception: Si le prenom n'est pas une chaîne de caractères.
            Exception: Si le pseudo n'est pas une chaîne de caractères ou si il contient des caractères spéciaux.
            Exception : Si l'adresse mail n'est pas une chaîne de caractères.
            Exception: Si la langue n'est pas une chaîne de caractères.
            Exception : Si le mot de passe n'est pas une chaîne de caractères.
            Exception: Si id_utilisateur n'est pas une chaîne de caractères.
        """

        if not isinstance(nom, str):
            raise Exception("Le nom n'est pas une chaîne de caractères.")
        if not isinstance(prenom, str):
            raise Exception("Le prenom n'est pas une chaîne de caractères.")
        if not isinstance(pseudo, str):
            raise Exception("Le pseudo n'est pas une chaîne de caractères.")
        for caractere in pseudo:
            if not (caractere.isalnum() or caractere == "_" or caractere == "."):
                raise Exception("Il y a des caratères non autorisés dans le pseudo")
        if not isinstance(adresse_mail, str):
            raise Exception("L'adresse mail n'est pas une chaîne de caractères.")
        if not isinstance(langue, str):
            raise Exception("La langue n'est pas une chaîne de caractères.")
        if not isinstance(mdp, str):
            raise Exception("Le mot de passe n'est pas une chaîne de caractères.")
        if not isinstance(id_utilisateur, int):
            raise Exception("id_utilisateur n'est pas un entier.")
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

    def message(self):
        """Permet d'afficher un message de bienvenue"""
        return f"Bienvenue {self.prenom} sur notre application !"

    def info_utilisateur(self) -> dict:
        """Retourne les attributs de l'utilisateur sous forme de dictionnaire"""
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
        return self.nom

    def get_prenom(self):
        return self.prenom

    def get_pseudo(self):
        return self.pseudo

    def get_adresse_mail(self):
        return self.adresse_mail

    def get_langue(self):
        return self.langue

    def get_id_utilisateur(self):
        return self.id_utilisateur

    def get_sel(self):
        return self.sel  # Ajout d'un getter pour récupérer le sel
