import re

import pytest

from src.webservice.business_object.abonnement import Abonnement


def test_abonnement_init_succes():
    Abonnement("abonnement_famille", 12.4, 2334, "detail_offre")


@pytest.mark.parametrize(
    "nom_abonnement, prix, id_abonnement, detail_offre, erreur, message_erreur",
    [
        (
            "abonnement_famille",
            12.4,
            {2334},
            "detail_offre",
            Exception,
            "L'identifiant de l'abonnement n'est pas un entier.",
        ),
    ],
)
def test_abonnement_init_echec(id_abonnement, erreur, message_erreur
):
    with pytest.raises(erreur, match=re.escape(message_erreur)):
        Abonnement(id_abonnement)


def test_info_abonnement():
    abonnement = Abonnement(2334)
    assert abonnement.info_abonnement() == {
        "Nom_abonnement": self.nom_abonnement,
        "prix": self.prix,
        "id_abonnement": 2334,
        "pub": self.pub,
        "qualité" : self.qualite,
    }


def test_get_prix():
    abonnement = Abonnement(2334)
    assert abonnement.get_nom_abonnement() == self.prix
