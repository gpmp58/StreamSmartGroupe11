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
    langue : str
        la langue parlée par l'utilisateur
    """

    def __init__(self, id_utilisateur=None, nom, prenom, adresse_mail, mdp=None, langue):
        """Constructeur"""
        self.id_utilisateur = id_utilisateur
        self.nom = nom
        self.prenom = prenom
        self.adresse_mail = adresse_mail
        self.mdp = mdp
        self.langue = langue

    def __str__(self):
        """Permet d'afficher les informations de l'utilisateur"""
        return f"Bienvenue {self.prenom} sur notre application !"

    def info_utilisateur(self) -> list[str]:
        """Retourne les attributs de l'utilisateur dans une liste"""
        return [self.id_utilisateur, self.nom, self.prenom, self.adresse_mail]