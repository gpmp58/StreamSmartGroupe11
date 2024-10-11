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
        self.id_utilisateur = id_utilisateur
        self.nom = nom
        self.prenom = prenom
        self.pseudo = pseudo
        self.adresse_mail
        self.mdp = mdp
        self.langue = langue
        

    def __str__(self):
        """Permet d'afficher les informations de l'utilisateur"""
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


    def get_adresse_mail(self):
        return self.adresse_mail
    
    def get_langue(self):
        return self.langue

    
