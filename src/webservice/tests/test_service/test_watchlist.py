import re

import pytest

from src.webservice.business_object.watchlist import Watchlist

from src.webservice.business_object.utilisateur import Utilisateur


def test_watchlist_init_succes():
    Watchlist(
        "watchlist_alice",
        123,
        ["film1", "film2"],
        1290,
    )


@pytest.mark.parametrize(
    "nom_watchlist , id_utilisateur, list_film , id_watchlist , erreur, message_erreur",
    [
        (
            {"watchlist_alice":""},
            123,
            ["film1", "film2"],
            1290,
            TypeError,
            "nom_watchlist doit être une chaîne de caractères, mais reçu dict"        
        ),
        (
            "watchlist_alice",
            "alice123",
            ["film1", "film2"],
            1290,
            TypeError,
            "id_utilisateur doit être un entier, mais reçu str",
        ),
        (
            "watchlist_alice",
            123,
            "film1",
            1290,
            TypeError,
            "list_film doit être une liste ou None, mais reçu str",
        ),
        (
            "watchlist_alice",
            123,
            ["film1", "film2"],
            {1290: ""},
            TypeError,
            "id_watchlist doit être un entier ou None, mais reçu dict",
        ),
    ],
)
def test_utilisateur_init_echec(
    nom_watchlist , id_utilisateur, list_film , id_watchlist , erreur, message_erreur
):
    with pytest.raises(erreur, match=re.escape(message_erreur)):
        Watchlist(nom_watchlist , id_utilisateur, list_film , id_watchlist)

def test_get_nom_watchlist():
    watchlist = Watchlist(
        "watchlist_alice",
        123,
        ["film1", "film2"],
        1290,
    )
    assert watchlist.get_nom_watchlist() == "watchlist_alice"  


def test_get_list_film():
    watchlist = Watchlist(
        "watchlist_alice",
        123,
        ["film1", "film2"],
        1290,
    )
    assert watchlist.get_list_film() == ["film1", "film2"]  

def test_verifier_utilisateur_succès():
    utilisateur = Utilisateur(
        "Dupont",
        "Alice",
        "alice123",
        "alice@example.com",
        "password123",
        1234,
    )
    watchlist = Watchlist("watchlist_alice", 1234, ["film1", "film2"], 1290)
    assert watchlist.verifier_utilisateur(utilisateur) == True

@pytest.mark.parametrize(
    "utilisateur , erreur, message_erreur",
    [
        (
            ["utilisateur"],
            TypeError,
            "utilisateur doit être une instance de Utilisateur"        
        ),
    ],
)
def test_verifier_utilisateur_echec(utilisateur , erreur, message_erreur):
    #GIVEN
    watchlist = Watchlist("watchlist_alice", 123, ["film1", "film2"], 1290)
    with pytest.raises(erreur, match=re.escape(message_erreur)):
        watchlist.verifier_utilisateur(utilisateur)