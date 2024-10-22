import re

import pytest

from src.webservice.business_object.abonnement import Abonnement


def test_abonnement_init_succes():
    Abonnement("abonnement_famille", 12.4, 2334, "detail_offre")


@pytest.mark.parametrize(
    "nom_abonnement, prix, id_abonnement, detail_offre, erreur, message_erreur",
    [
        (
            ["abonnement_famille"],
            12.4,
            2334,
            "detail_offre",
            Exception,
            "Le nom de l'abonnement n'est pas une chaîne de caractères.",
        ),
        (
            "abonnement_famille",
            "12.4",
            2334,
            "detail_offre",
            Exception,
            "Le prix de l'abonnement n'est pas un flottant.",
        ),
        (
            "abonnement_famille",
            12.4,
            {2334},
            "detail_offre",
            Exception,
            "L'identifiant de l'abonnement n'est pas une chaîne de caractères.",
        ),
        (
            "abonnement_famille",
            12.4,
            2334,
            2527,
            Exception,
            "Le detail de l'offre n'est pas une chaîne de caractères.",
        ),
    ],
)
def test_abonnement_init_echec(
    nom_abonnement, prix, id_abonnement, detail_offre, erreur, message_erreur
):
    with pytest.raises(erreur, match=re.escape(message_erreur)):
        Abonnement(nom_abonnement, prix, id_abonnement, detail_offre)


def test_info_abonnement():
    abonnement = Abonnement("abonnement_famille", 12.4, 2334, "detail_offre")
    assert abonnement.info_abonnement() == {
        "Nom_abonnement": "abonnement_famille",
        "prix": 12.4,
        "id_abonnement": 2334,
        "detail_offre": "detail_offre",
    }


def test_get_nom_abonnement():
    abonnement = Abonnement("abonnement_famille", 12.4, 2334, "detail_offre")
    assert abonnement.get_nom_abonnement() == "abonnement_famille"
