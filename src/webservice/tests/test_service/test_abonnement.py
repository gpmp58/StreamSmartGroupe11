import re

import pytest

from src.webservice.business_object.abonnement import Abonnement
from src.webservice.dao.abonnement_dao import AbonnementDao


@pytest.mark.parametrize(
    "id_abonnement, nom_plateforme, erreur, message_erreur",
    [
        (
            {2334},
            "Netflix",
            Exception,
            "L'identifiant de l'abonnement n'est pas un entier.",
        ),
        (
            2334,
            ["Netflix"],
            Exception,
            "Le nom de la plateforme n'est pas une chaîne de caractère.",
        ),
    ],
)
def test_abonnement_init_echec(
        id_abonnement,
        nom_plateforme,
        erreur,
        message_erreur):
    with pytest.raises(erreur, match=re.escape(message_erreur)):
        Abonnement(id_abonnement, nom_plateforme)


def test_info_abonnement():
    abonnement = Abonnement(1, "Amazon")
    assert abonnement.info_abonnement() == {
        "Nom_abonnement": "Avec pub",
        "prix": 6.99,
        "id_abonnement": 1,
        "pub": True,
        "qualité": "4K",
    }


def test_get_prix():
    abonnement = Abonnement(5, "Canal+")
    assert abonnement.get_prix() == 19.99


def test_get_nom_abonnement():
    abonnement = Abonnement(1, "Amazon")
    assert abonnement.get_nom_abonnement() == "Avec pub"


def test_get_id_abonnement():
    abonnement = Abonnement(1, "Amazon")
    assert abonnement.get_id_abonnement() == 1


def test_get_qualite():
    abonnement = Abonnement(1, "Amazon")
    assert abonnement.get_qualite() == "4K"


def test_get_pub():
    abonnement = Abonnement(1, "Amazon")
    assert abonnement.get_pub()
