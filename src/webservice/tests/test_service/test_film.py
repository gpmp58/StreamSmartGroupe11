import re

import pytest
from src.webservice.business_object.film import Film


@pytest.mark.parametrize(
    " id_film ,erreur, message_erreur",
    [
        ({"268"}, TypeError, "id_film doit être un entier"),
    ],
)
def test_film_init_echec(id_film, erreur, message_erreur):
    with pytest.raises(erreur, match=re.escape(message_erreur)):
        Film(id_film)


def succes_init_film():
    id_film = 268
    film_test = Film(id_film)
    assert film_test.id_film == 268
    assert (
        film_test.image == "https://image.tmdb.org/t/"
        "p/w600_and_h900_bestv2/cij4dd21v2Rk2YtUQbV5kW69WB2.jpg"
    )
    assert film_test.streaming == [
        {
            "id": 381,
            "name": "Canal+",
            "logo": "https://image.tmdb.org"
            "/t/p/w780/eBXzkFEupZjKaIKY7zBUaSdCY8I.jpg",
        },
        {
            "id": 1899,
            "name": "Max",
            "logo": "https://image.tmdb.org/"
            "t/p/w780/fksCUZ9QDWZMUwL2LgMtLckROUN.jpg",
        },
    ]


def test_afficher():
    id_film = 268
    film_test = Film(id_film)
    details = film_test.afficher_film()
    assert details == {
        "name": "Batman",
        "description": "Violence et corruption "
        "règnent dans la ville de Gotham City. La mafia dirige la ville"
        " à sa manière, au nez et à la barbe des autorités,"
        " complètement"
        " dépassées par les événements. Depuis quelques "
        "semaines cependant, "
        "un mystérieux justicier, drapé dans un costume de chauve-souris, "
        "terrorise les malfaiteurs et sème l'inquiétude dans "
        "les rangs de la mafia."
        " Une jeune journaliste, Vicki Vale, mène l'enquête."
        " C'est ainsi qu'elle "
        "fait la connaissance d'un séduisant mais excentrique "
        "milliardaire, Bruce Wayne"
        ". Celui-ci n'est autre que Batman, qui l'a déjà sauvée."
        " Elle rencontre "
        "également un odieux truand, Jack Napier, bras droit du "
        "parrain Carl Grissom...",
        "sortie": "Released",
        "vote_average": 7.23,
        "date_sortie": "21/06/1989",
        "duree": "2 h 6 min",
        "genres": ["Fantastique", "Action", "Crime"],
    }
