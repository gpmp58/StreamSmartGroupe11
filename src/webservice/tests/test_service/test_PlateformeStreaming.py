import re

import pytest

from src.webservice.business_object.PlateformeStreaming import PLateformeStreaming


def test_PlateformeStreaming_init_succes():
    PLateformeStreaming("Netflix", "logo_plateforme", 1230)

@pytest.mark.parametrize(
    "nom_plateforme, logo_plateforme, id_plateforme, erreur, message_erreur",
    [
        ([Netflix], "logo_plateforme", 1230, Exception, "Le nom de la plateforme n'est pas une chaîne de caractères."),
        ("Netflix", {logo_plateforme}, 1230, Exception,"Le logo de la plateforme n'est pas une chaîne de caractères."),
        ("Netflix", "logo_plateforme", "1230", Exception, "L'identifiant de la plateforme n'est pas un entier."),
    ],
)


def test_PlateformeStreaming_init_echec(nom_plateforme, logo_plateforme, id_plateforme, erreur, message_erreur):
    with pytest.raises(erreur, match=re.escape(message_erreur)):
        PLateformeStreaming(nom_plateforme, logo_plateforme, id_plateforme)


def test_info_film(self):
    plateforme = PLateformeStreaming("Netflix", "logo_plateforme", 1230)
    self.assertEqual(info_plateforme(plateforme), {
            "Nom_plateforme": "Netflix",
            "logo_plateforme": "logo_plateforme",
            "id_plateforme": 1230,
        })


def test_get_nom_plateforme(self):
    plateforme = PLateformeStreaming("Netflix", "logo_plateforme", 1230)
    self.assertEqual(get_nom_plateforme(plateforme), "Netflix")