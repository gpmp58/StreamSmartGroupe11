import re

import pytest

from src.webservice.business_object.critere import Critere
from src.webservice.business_object.watchlist import Watchlist


def test_critere_init_succes():
    Critere(2346, {"qualite": "4K", "pub": True,
                   "prix": True, "rapport_quantite_prix": False}, )


@pytest.mark.parametrize("id_watchlist, criteres, erreur, message_erreur",
                         [(["id_watchlist"],
                           {"qualite": "4K",
                            "pub": True,
                            "prix": True,
                             "rapport_quantite_prix": False,
                            },
                             Exception,
                             "L'id watchlist n'est pas un entier.",
                           ),
                             (2345,
                              1230,
                              Exception,
                              "criteres n'est pas un dictionnaire.",
                              ),
                             (2345,
                              {"quantité": "4K",
                               "pub": True,
                               "prix": True,
                               "rapport_quantite_prix": False,
                               },
                              Exception,
                              "Clé quantité inconnue dans les critères.",
                              ),
                             (2345,
                              {"qualite": 2,
                               "pub": True,
                               "prix": True,
                               "rapport_quantite_prix": False},
                              Exception,
                              "La valeur de la clé qualite n'est pas du type str.",
                              ),
                             (2345,
                              {"qualite": "4K",
                               "pub": "True",
                               "prix": True,
                               "rapport_quantite_prix": False,
                               },
                              Exception,
                              "La valeur de la clé pub n'est pas du type bool.",
                              ),
                             (2345,
                              {"qualite": "4K",
                               "pub": True,
                               "prix": 2,
                               "rapport_quantite_prix": False},
                              Exception,
                              "La valeur de la clé prix n'est pas du type bool.",
                              ),
                             (2345,
                              {"qualite": "HD",
                               "pub": True,
                               "prix": True,
                               "rapport_quantite_prix": 23},
                              Exception,
                              "La valeur de la clé rapport_quantite_prix n'est pas du type bool.",
                              ),
                          ],
                         )
def test_critere_init_echec(id_watchlist, criteres, erreur, message_erreur):
    with pytest.raises(erreur, match=re.escape(message_erreur)):
        Critere(id_watchlist, criteres)


def test_get_id_watchlist():
    critere = Critere(2345,
                      {"qualite": "4K",
                       "pub": True,
                       "prix": True,
                       "rapport_quantite_prix": False},
                      )
    assert critere.get_id_watchlist() == 2345


def test_get_critere():
    critere = Critere(2345,
                      {"qualite": "4K",
                       "pub": True,
                       "prix": True,
                       "rapport_quantite_prix": False},
                      )
    assert critere.get_critere() == {
        "qualite": "4K",
        "pub": True,
        "prix": True,
        "rapport_quantite_prix": False,
    }
