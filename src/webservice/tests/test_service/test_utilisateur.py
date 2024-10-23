import re

import pytest

from src.webservice.business_object.utilisateur import Utilisateur


def test_utilisateur_init_succes():
    Utilisateur(
        "Dupont",
        "Alice",
        "alice123",
        "alice@example.com",
        "password123",
        1234,
    )


@pytest.mark.parametrize(
    "nom, prenom, pseudo, adresse_mail, mdp, id_utilisateur, erreur, message_erreur",
    [
        (
            ["Dupont"],
            "Alice",
            "alice123",
            "alice@example.com",
            "password123",
            1234,
            Exception,
            "Le nom n'est pas une chaîne de caractères.",
        ),
        (
            "Dupont",
            {"Alice"},
            "alice123",
            "alice@example.com",
            "password123",
            1234,
            Exception,
            "Le prenom n'est pas une chaîne de caractères.",
        ),
        (
            "Dupont",
            "Alice",
            ["a", "lic", "e1", "23"],
            "alice@example.com",
            "password123",
            1234,
            Exception,
            "Le pseudo n'est pas une chaîne de caractères.",
        ),
        (
            "Dupont",
            "Alice",
            "alice@&",
            "alice@example.com",
            "password123",
            1234,
            Exception,
            "Il y a des caratères non autorisés dans le pseudo",
        ),
        (
            "Dupont",
            "Alice",
            "alice123",
            23,
            "password123",
            1234,
            Exception,
            "L'adresse mail n'est pas une chaîne de caractères.",
        ),
        (
            "Dupont",
            "Alice",
            "alice123",
            "alice@example.com",
            12,
            1234,
            Exception,
            "Le mot de passe n'est pas une chaîne de caractères.",
        ),
        (
            "Dupont",
            "Alice",
            "alice123",
            "alice@example.com",
            "password123",
            "1234",
            Exception,
            "id_utilisateur n'est pas un entier.",
        ),
    ],
)
def test_utilisateur_init_echec(
    nom, prenom, pseudo, adresse_mail, mdp, id_utilisateur, erreur, message_erreur
):
    with pytest.raises(erreur, match=re.escape(message_erreur)):
        Utilisateur(nom, prenom, pseudo, adresse_mail, mdp, id_utilisateur)


def test_message():
    utilisateur = Utilisateur(
        "Dupont",
        "Alice",
        "alice123",
        "alice@example.com",
        "password123",
        "id_utilisateur",
    )
    assert utilisateur.message() == "Bienvenue Alice sur notre application !"


def test_info_utilisateur():
    utilisateur = Utilisateur(
        "Dupont",
        "Alice",
        "alice123",
        "alice@example.com",
        "password123",
        "id_utilisateur",
    )
    assert utilisateur.info_utilisateur() == {
        "Nom": "Dupont",
        "Prénom": "Alice",
        "Pseudo": "alice123",
        "Adresse mail": "alice@example.com",
        "Langue": "français",
        "id_utilisateur": "id_utilisateur",
    }


def test_get_nom():
    utilisateur = Utilisateur(
        "Dupont",
        "Alice",
        "alice123",
        "alice@example.com",
        "password123",
        "id_utilisateur",
    )
    assert utilisateur.get_nom() == "Dupont"
