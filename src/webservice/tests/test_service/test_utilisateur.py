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
            "L'identifiant de l'utilisateur n'est pas un entier.",
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
        1234,
    )
    assert utilisateur.message() == "Bienvenue Alice sur notre application !"


def test_info_utilisateur():
    utilisateur = Utilisateur(
        "Dupont",
        "Alice",
        "alice123",
        "alice@example.com",
        "password123",
        1234,
        "français",
        "selalice",
    )
    assert utilisateur.info_utilisateur() == {
        "Nom": "Dupont",
        "Prénom": "Alice",
        "Pseudo": "alice123",
        "Adresse mail": "alice@example.com",
        "Langue": "français",
        "id_utilisateur": 1234,
        "sel": "selalice",
    }


def test_get_nom():
    utilisateur = Utilisateur(
        "Dupont",
        "Alice",
        "alice123",
        "alice@example.com",
        "password123",
        1234,
    )
    assert utilisateur.get_nom() == "Dupont"


def test_get_prenom():
    utilisateur = Utilisateur(
        "Dupont",
        "Alice",
        "alice123",
        "alice@example.com",
        "password123",
        1234,
    )
    assert utilisateur.get_prenom() == "Alice"

def test_get_pseudo():
    utilisateur = Utilisateur(
        "Dupont",
        "Alice",
        "alice123",
        "alice@example.com",
        "password123",
        1234,
    )
    assert utilisateur.get_pseudo() == "alice123"

def test_get_adresse_mail():
    utilisateur = Utilisateur(
        "Dupont",
        "Alice",
        "alice123",
        "alice@example.com",
        "password123",
        1234,
    )
    assert utilisateur.get_adresse_mail() == "alice@example.com"

def test_get_langue():
    utilisateur = Utilisateur(
        "Dupont",
        "Alice",
        "alice123",
        "alice@example.com",
        "password123",
        1234,
    )
    assert utilisateur.get_langue() == "français"


def test_get_id_utilisateur():
    utilisateur = Utilisateur(
        "Dupont",
        "Alice",
        "alice123",
        "alice@example.com",
        "password123",
        1234,
    )
    assert utilisateur.get_id_utilisateur() == 1234

def test_get_sel():
    utilisateur = Utilisateur(
        "Dupont",
        "Alice",
        "alice123",
        "alice@example.com",
        "password123",
        1234,
    )
    assert utilisateur.get_sel() == None
