import re

import pytest

from src.webservice.business_object.utilisateur import Utilisateur


def test_utilisateur_init_succes():
    Utilisateur("Dupont", "Alice", "alice123", "alice@example.com", "password123", "id_utilisateur")

@pytest.mark.parametrize(
    "nom, prenom, pseudo, adresse_mail, mdp, id_utilisateur, erreur, message_erreur",
    [
        ([Dupont],"Alice", "alice123", "alice@example.com", "password123", "id_utilisateur", Exception, "Le nom n'est pas une chaîne de caractères."),
        ("Dupont", {Alice}, "alice123", "alice@example.com", "password123", "id_utilisateur", Exception,"Le prenom n'est pas une chaîne de caractères."),
        ("Dupont","Alice", [a, lic, e1, 23], "alice@example.com", "password123", "id_utilisateur", Exception, "Le pseudo n'est pas une chaîne de caractères."),
        ("Dupont","Alice", "alice@&", "alice@example.com", "password123", "id_utilisateur", Exception, "Il y a des caratères non autorisés dans le pseudo")
        ("Dupont","Alice", "alice123", 23, "password123", "id_utilisateur", Exception, "L'adresse mail n'est pas une chaîne de caractères."),
        ("Dupont","Alice", "alice123", "alice@example.com", 12, "id_utilisateur", Exception, "Le mot de passe n'est pas une chaîne de caractères."),
        ("Dupont","Alice", "alice123", "alice@example.com", "password123", 1234, Exception, "id_utilisateur n'est pas une chaîne de caractères."),
    ],
)


def test_utilisateur_init_echec(nom, prenom, pseudo, adresse_mail, mdp, id_utilisateur, erreur, message_erreur):
    with pytest.raises(erreur, match=re.escape(message_erreur)):
        Utilisateur(nom, prenom, pseudo, adresse_mail, mdp, id_utilisateur)


def test__str__(self):
    utilisateur = Utilisateur("Dupont", "Alice", "alice123", "alice@example.com", "password123", "id_utilisateur")
    self.assertEqual(__str__(utilisateur), "Bienvenue Alice sur notre application !")


def test_info_utilisateur(self):
    utilisateur = Utilisateur("Dupont", "Alice", "alice123", "alice@example.com", "password123", "id_utilisateur")
    self.assertEqual(info_utilisateur(utilisateur), {
            "Nom": "Dupont",
            "Prénom": "Alice",
            "Pseudo": "alice123",
            "Adresse mail": "alice@example.com",
            "Langue":"français",
            "id_utilisateur": "id_utilisateur",
        })


def test_get_nom(self):
    utilisateur = Utilisateur("Dupont", "Alice", "alice123", "alice@example.com", "password123", "id_utilisateur")
    self.assertEqual(get_nom(utilisateur), "Dupont")