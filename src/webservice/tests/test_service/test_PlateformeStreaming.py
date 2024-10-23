import re

import pytest

from src.webservice.business_object.plateforme import PlateformeStreaming


def test_PlateformeStreaming_init_succes():
    PlateformeStreaming("Netflix", 1230, "logo_plateforme")


@pytest.mark.parametrize(
    "nom_plateforme, id_plateforme, logo_plateforme, erreur, message_erreur",
    [
        (
            ["Netflix"],
            1230,
            "logo_plateforme",
            Exception,
            "Le nom de la plateforme n'est pas une chaîne de caractères.",
        ),
        (
            "Netflix",
            1230,
            {"logo_plateforme"},
            Exception,
            "Le logo de la plateforme n'est pas une chaîne de caractères ou n'est pas égal à None.",
        ),
        (
            "Netflix",
            "1230",
            "logo_plateforme",
            Exception,
            "L'identifiant de la plateforme n'est pas un entier.",
        ),
    ],
)
def test_PlateformeStreaming_init_echec(
    nom_plateforme, logo_plateforme, id_plateforme, erreur, message_erreur
):
    with pytest.raises(erreur, match=re.escape(message_erreur)):
        PlateformeStreaming(nom_plateforme, logo_plateforme, id_plateforme)


def test_info_plateforme():
    plateforme = PlateformeStreaming("Netflix", 1230, "logo_plateforme")
    assert plateforme.info_plateforme() == {
        "Nom_plateforme": "Netflix",
        "id_plateforme": 1230,
        "logo_plateforme": "logo_plateforme",
    }


def test_get_nom_plateforme():
    plateforme = PlateformeStreaming("Netflix", 1230, "logo_plateforme")
    assert plateforme.get_nom_plateforme() == "Netflix"
