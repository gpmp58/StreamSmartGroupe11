import re

import pytest

from src.webservice.business_object.abonnement import Abonnement
from src.webservice.dao.abonnement_dao import AbonnementDao


def test_abonnement_init_succes():
    Abonnement(2334, "Netflix")


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
def test_abonnement_init_echec(id_abonnement, nom_plateforme, erreur, message_erreur
):
    with pytest.raises(erreur, match=re.escape(message_erreur)):
        Abonnement(id_abonnement, nom_plateforme)


def test_info_abonnement():
    abonnement = Abonnement(2334, "Netflix")
    assert abonnement.info_abonnement() == {
        "Nom_abonnement": AbonnementDao().get_nom_abonnement_DAO(2334),
        "prix": AbonnementDao().get_prix_abonnement_DAO(2334),
        "id_abonnement": 2334,
        "pub": AbonnementDao().get_pub_abonnement_DAO(2334),
        "qualité" : AbonnementDao().get_qualite_abonnement_DAO(2334),
    }


def test_get_prix():
    abonnement = Abonnement(2334, "Netflix")
    assert abonnement.get_prix() == AbonnementDao().get_prix_abonnement_DAO(2334)


def test_get_nom_abonnement():
    abonnement = Abonnement(2334, "Netflix")
    assert abonnement.get_nom_abonnement() == AbonnementDao().get_nom_abonnement_DAO(2334)


def test_get_id_abonnement():
    abonnement = Abonnement(2334, "Netflix")
    assert abonnement.get_id_abonnement() == 2334


def test_get_qualite():
    abonnement = Abonnement(2334, "Netflix")
    assert abonnement.get_qualite() == AbonnementDao().get_qualite_abonnement_DAO(2334)


def test_get_pub():
    abonnement = Abonnement(2334, "Netflix")
    assert abonnement.get_pub() ==AbonnementDao().get_pub_abonnement_DAO(2334)
