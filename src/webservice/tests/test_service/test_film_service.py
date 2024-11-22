import re

import pytest

from src.webservice.services.service_film import FilmService

def test_service_film_init_succes():
    FilmService(
        "Joker",
    )


@pytest.mark.parametrize(
    "nom_film, erreur, message_erreur",
    [
        (
            ["Joker"],
            TypeError,
            "Le film doit être en format caractères",
        ),
        (
            "J@oker",
            Exception,
            "Il y a des caratères spéciaux dans le film, Veuillez réécrire le nom du film",
        ),
    ],
)
def test_utilisateur_init_echec(
    nom_film, erreur, message_erreur
):
    with pytest.raises(erreur, match=re.escape(message_erreur)):
        FilmService(nom_film)

def test_rechercher_film():
    nom_film = "Cargo"
    service = FilmService(nom_film)
    resultat = service.rechercher_film()
    assert "Cargo" in resultat.values()