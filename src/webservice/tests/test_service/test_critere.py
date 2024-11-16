import re

import pytest

from src.webservice.business_object.critere import Critere
from src.webservice.business_object.watchlist import Watchlist


def test_critere_init_succes():
    Critere(Watchlist("nom_watch", 2345, [], None), {"qualité" : "qualité", "pub": True, "prix" : True, "rapport_quantite_prix": False})

@pytest.mark.parametrize(
    "watchlist, criteres, erreur, message_erreur",
    [
        (
            ["watchlist"],
            {"qualité" : "qualité", "pub": True, "prix" : True, "rapport_quantite_prix": False},
            Exception,
            "La watchlist n'est pas une instance Watchlist.",
        ),
        (
            Watchlist('nom_watch', 2345, [], None),
            1230,
            Exception,
            "criteres n'est pas un dictionnaire.",
        ),
        (
            Watchlist("nom_watch", 2345, [], None),
            {"qualité" : 2, "pub": True, "prix" : True, "rapport_quantite_prix": False},
            Exception,
            "La valeur de la clé qualité n'est pas du type str.",
        ),
        (
            Watchlist("nom_watch", 2345, [], None),
            {"qualité" : "qualité", "pub": "True", "prix" : True, "rapport_quantite_prix": False},
            Exception,
            "La valeur de la clé pub n'est pas du type bool.",
        ),
        (
            Watchlist("nom_watch", 2345, [], None),
            {"qualité" : 2, "pub": True, "prix" : {"True": True}, "rapport_quantite_prix": False},
            Exception,
            "La valeur de la clé prix n'est pas du type bool.",
        ),
        (
            Watchlist("nom_watch", 2345, [], None),
            {"qualité" : "qualité", "pub": True, "prix" : True, "rapport_quantite_prix": 23},
            Exception,
            "La valeur de la clé rapport_quantite_prix n'est pas du type bool.",
        ),
    ],
)
def test_critere_init_echec(
    watchlist, criteres, erreur, message_erreur
):
    with pytest.raises(erreur, match=re.escape(message_erreur)):
        Critere(watchlist, criteres)

def test_get_watchlist():
    critere = Critere(Watchlist("nom_watch", 2345, [], None), {"qualité" : "qualité", "pub": True, "prix" : True, "rapport_quantite_prix": False})
    assert critere.get_watchlist() == Watchlist("nom_watch", 2345, [], None)

def test_get_critere():
    critere = Critere(Watchlist("nom_watch", 2345, [], None), {"qualité" : "qualité", "pub": True, "prix" : True, "rapport_quantite_prix": False})
    assert critere.get_critere() == {"qualité" : "qualité", "pub": True, "prix" : True, "rapport_quantite_prix": False}
