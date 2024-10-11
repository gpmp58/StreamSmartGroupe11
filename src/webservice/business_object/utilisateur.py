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
    """

    def __init__(self, nom, prenom, pseudo, adresse_mail, mdp=None,  ):
        """Constructeur"""
        self.nom = nom
        self.prenom = prenom
        self.pseudo = pseudo
        self.adresse_mail = adresse_mail
        self.mdp = mdp
        

    def __str__(self):
        """Permet d'afficher les informations de l'utilisateur"""
        return f"Bienvenue {self.prenom} sur notre application !"

    def info_utilisateur(self) -> list[str]:
        """Retourne les attributs de l'utilisateur dans une liste"""
        return [self.nom, self.prenom, self.pseudo, self.adresse_mail]
