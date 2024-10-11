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
    """

    def __init__(self, nom: str, prenom: str, pseudo: str, adresse_mail: str, mdp=None, id_utilisateur=None, langue: str = "français"):
        """Constructeur avec validation basique"""
         """
        Initialise un objet Utilisateur avec les attributs spécifiés.

        Args:
            nom (str) : Le nom renseigné par l'utilisateur.
            prenom (str) : Le prenom renseigné par l'utilisateur.
            pseudo (str) : Le pseudo renseigné par l'utilisateur.
            adresse_mail (str) : L'adresse mail renseignée par l'utilisateur.
            langue (str) : La langue de renseignée par l'utilisateur, si différente de celle par défaut.

        Raises:
            Exception: Si le nom n'est pas une chaîne de caractères.
            Exception: Si le prenom n'est pas une chaîne de caractères.
            Exception: Si le peudo n'est pas une chaîne de caractères ou si il contient des caractères spéciaux.
            # a voir si on ajoute des conditions sur le pseudo 
            Exception : Si l'adresse mail n'est pas une chaîne de caractères.
            Exception: Si la langue n'est pas une chaîne de caractères.
        """

        if not isinstance(nom, str):
            raise Exception("Le nom n'est pas une chaîne de caractères.")
        if not isinstance(prenom, str):
            raise Exception("Le prenom n'est pas une chaîne de caractères.")
        if not isinstance(pseudo, str):
            raise Exception("Le pseudo n'est pas une chaîne de caractères.")
        for caractere in pseudo :
            if not (caractere.isalnum() or caractere == "_" or caractere == ".") :
                raise Exception("Il y a des caratères non autorisés dans le pseudo")
        if not isinstance(adresse_mail, str):
            raise Exception("L'adresse mail n'est pas une chaîne de caractères.")
        if not isinstance(langue, str):
            raise Exception("La langue n'est pas une chaîne de caractères.")

        self.id_utilisateur = id_utilisateur
        self.nom = nom
        self.prenom = prenom
        self.pseudo = pseudo
        self.adresse_mail
        self.mdp = mdp
        self.langue = langue
        

    def __str__(self):
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
        }

    def get_nom(self):
        return self.nom

    def get_prenom(selft): 
        return self.prenom

    def get_pseudo(selft):
        return self.pseudo
    
    def get_adresse_mail(self):
        return self.adresse_mail
    
    def get_langue(self):
        return self.langue

    def get_id_utilisateur(self):
        return self.id_utilisateur    

