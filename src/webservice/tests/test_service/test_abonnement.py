import re

import pytest

from src.webservice.business_object.abonnement import Abonnement


def test_abonnement_init_succes():
    Abonnement(2334, "abonnement_familial", "HD", 12.3, True)


@pytest.mark.parametrize(
    "id_abonnement, nom_abonnement, qualité, prix, pub, erreur, message_erreur",
    [
        (
            {2334},
            "abonnement_familial",
            "HD",
            12.3,
            True, 
            Exception,
            "L'identifiant de l'abonnement n'est pas un entier.",
        ),
        (
            2334,
            ["abonnement_familial"],
            "HD",
            12.3,
            True, 
            Exception,
            "Le nom de l'abonnement n'est pas une chaîne de caractère.",
        ),
        (
            {2334},
            "abonnement_familial",
            "HD",
            12.3,
            True, 
            Exception,
            "L'identifiant de l'abonnement n'est pas un entier.",
        ),
        (
            2334,
            "abonnement_familial",
            1,
            12.3,
            True, 
            Exception,
            "La qualité de l'abonnement n'est pas une chaîne de caractère.",
        ),
        (
            2334,
            "abonnement_familial",
            "HD",
            3,
            True, 
            Exception,
            "Le prix de l'abonnement n'est pas un nombre.",
        ),
        (
            2334,
            "abonnement_familial",
            "HD",
            12.3,
            [12], 
            Exception,
            "Pub n'est pas un booléen.",
        ),

    ],
)
def test_abonnement_init_echec(id_abonnement, nom_abonnement, qualité, prix, pub,erreur, message_erreur
):
    with pytest.raises(erreur, match=re.escape(message_erreur)):
        Abonnement(id_abonnement, nom_abonnement, qualité, prix, pub)


def test_info_abonnement():
    abonnement = Abonnement(2334, "abonnement_familial", "HD", 12.3, True)
    assert abonnement.info_abonnement() == {
        "Nom_abonnement": "abonnement_familial",
        "prix": 12.3,
        "id_abonnement": 2334,
        "pub": True,
        "qualité" : "HD",
    }


def test_get_prix():
    abonnement = Abonnement(2334, "abonnement_familial", "HD", 12.3, True)
    assert abonnement.get_prix() == 12.3


def test_get_nom_abonnement():
    abonnement = Abonnement(2334, "abonnement_familial", "HD", 12.3, True)
    assert abonnement.get_nom_abonnement() == "abonnement_familial"


def test_get_id_abonnement():
    abonnement = Abonnement(2334, "abonnement_familial", "HD", 12.3, True)
    assert abonnement.get_id_abonnement() == 2334


def test_get_qualite():
    abonnement = Abonnement(2334, "abonnement_familial", "HD", 12.3, True)
    assert abonnement.get_qualite() == "HD"


def test_get_pub():
    abonnement = Abonnement(2334, "abonnement_familial", "HD", 12.3, True)
    assert abonnement.get_pub() == True
