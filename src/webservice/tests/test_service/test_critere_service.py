from src.webservice.services.service_critere import CritereService
from src.webservice.business_object.critere import Critere
from src.webservice.business_object.abonnement import Abonnement
from src.webservice.business_object.watchlist import Watchlist
from unittest.mock import patch
import pytest


@pytest.fixture
def service():
    return CritereService()


@patch(
    "src.webservice.services.service_watchlist."
    "WatchlistService.trouver_par_id"
)
@patch(
    "src.webservice.services.service_watchlist."
    "WatchlistService.sauvegarder_watchlist"
)
@patch("src.webservice.business_object.film.Film.recuperer_streaming")
def test_recuperer_plateformes_film(
    mock_recuperer_streaming,
    mock_sauvegarder_watchlist,
    mock_trouver_par_id,
    service,
):
    id_watchlist = 1
    critere = Critere(
        1,
        {
            "qualite": "qualité",
            "pub": True,
            "prix": True,
            "rapport_quantite_prix": False,
        },
    )

    watchlist_mock = Watchlist("test", 1, [], 1)
    films_mock = [{"id_film": 268, "nom_film": "Batman"}]
    plateformes_mock_101 = [
        {
            "id": 381,
            "name": "Canal+",
            "logo": "https://image.tmdb.org/t/"
            "p/w780/eBXzkFEupZjKaIKY7zBUaSdCY8I.jpg",
        },
        {
            "id": 1899,
            "name": "Max",
            "logo": "https://image.tmdb.org/t/p"
            "/w780/fksCUZ9QDWZMUwL2LgMtLckROUN.jpg",
        },
    ]
    mock_trouver_par_id.return_value = watchlist_mock
    mock_sauvegarder_watchlist.return_value = films_mock
    mock_recuperer_streaming.return_value = plateformes_mock_101

    resultat = service.recuperer_plateformes_film(critere)

    # Vérifications
    assert resultat == {268: ["Canal+", "Max"]}

    # Vérifie les appels des mocks
    mock_trouver_par_id.assert_called_once_with(id_watchlist)
    mock_sauvegarder_watchlist.assert_called_once_with(watchlist_mock)


@patch(
    "src.webservice.dao.abonnement_dao.AbonnementDao.abonnement_filtrés"
)
def test_filtrer_abonnement(mock_abonnement_filtrees):
    criteres = Critere(
        1,
        {
            "qualite": "4K",
            "pub": True,
            "prix": False,
            "rapport_quantite_prix": False,
        },
    )
    abonnement_mock = [
        {
            "id_abonnement": 1,
            "nom_plateforme": "Amazon",
            "prix": "6.99",
        }
    ]
    mock_abonnement_filtrees.return_value = abonnement_mock
    service = CritereService()
    resultat = service.filtrer_abonnement(criteres)
    assert resultat == abonnement_mock


@patch(
    "src.webservice.services.service_critere."
    "CritereService.filtrer_abonnement"
)
@patch(
    "src.webservice.services.service_critere."
    "CritereService.recuperer_plateformes_film"
)
def test_calculer_occurrences_plateformes(
    mock_recuperer_plateformes_film, mock_filtrer_abonnement
):
    criteres = Critere(
        1,
        {
            "qualite": "HD",
            "pub": True,
            "prix": False,
            "rapport_quantite_prix": False,
        },
    )

    mock_filtrer_abonnement.return_value = [
        {
            "id_abonnement": 14,
            "nom_plateforme": "Disney+",
            "prix": "5.99",
        },
        {
            "id_abonnement": 17,
            "nom_plateforme": "Netflix",
            "prix": "5.99",
        },
        {
            "id_abonnement": 20,
            "nom_plateforme": "Max",
            "prix": "5.99",
        },
        {
            "id_abonnement": 1,
            "nom_plateforme": "Amazon",
            "prix": "6.99",
        },
    ]
    mock_recuperer_plateformes_film.return_value = {
        268: ["Canal+", "Max"]
    }

    critere_service = CritereService()

    # Appel de la méthode à tester
    occurrences = critere_service.calculer_occurrences_plateformes(
        criteres
    )

    # Assertions
    assert occurrences == {"Max": 1}
    mock_filtrer_abonnement.assert_called_once_with(criteres)
    mock_recuperer_plateformes_film.assert_called_once_with(criteres)


@patch(
    "src.webservice.services.service_critere.CritereService.filtrer_abonnement"
)
@patch(
    "src.webservice.services.service_critere."
    "CritereService.calculer_occurrences_plateformes"
)
def test_optimiser_abonnement_nb_films(
    mock_calculer_occurrences,
    mock_filtrer_abonnement,
):
    # Préparer les données fictives
    criteres = Critere(
        1,
        {
            "qualite": "HD",
            "pub": True,
            "prix": False,
            "rapport_quantite_prix": False,
        },
    )

    mock_filtrer_abonnement.return_value = [
        {
            "id_abonnement": 14,
            "nom_plateforme": "Disney+",
            "prix": 5.99,
        },
        {
            "id_abonnement": 17,
            "nom_plateforme": "Netflix",
            "prix": 5.99,
        },
        {"id_abonnement": 20, "nom_plateforme": "Max", "prix": 5.99},
        {
            "id_abonnement": 1,
            "nom_plateforme": "Amazon",
            "prix": 6.99,
        },
    ]

    mock_calculer_occurrences.return_value = {
        "Max": 1,
        "Disney+": 2,
        "Netflix": 2,
        "Amazon": 1,
    }
    critere_service = CritereService()
    abonnement = critere_service.optimiser_abonnement(criteres)

    assert isinstance(abonnement, Abonnement)
    assert abonnement.nom_plateforme == "Disney+"
    assert abonnement.id_abonnement == 14
    mock_filtrer_abonnement.assert_called_once_with(criteres)
    mock_calculer_occurrences.assert_called_once_with(criteres)


@patch(
    "src.webservice.services.service_critere.CritereService.filtrer_abonnement"
)
@patch(
    "src.webservice.services.service_critere."
    "CritereService.calculer_occurrences_plateformes"
)
def test_optimiser_abonnement_prix(
    mock_calculer_occurrences,
    mock_filtrer_abonnement,
):
    # Préparer les données fictives
    criteres = Critere(
        1,
        {
            "qualite": "HD",
            "pub": True,
            "prix": True,
            "rapport_quantite_prix": False,
        },
    )

    mock_filtrer_abonnement.return_value = [
        {
            "id_abonnement": 14,
            "nom_plateforme": "Disney+",
            "prix": 10.99,
        },
        {
            "id_abonnement": 17,
            "nom_plateforme": "Netflix",
            "prix": 7.99,
        },
        {"id_abonnement": 20, "nom_plateforme": "Max", "prix": 5.99},
        {
            "id_abonnement": 1,
            "nom_plateforme": "Amazon",
            "prix": 6.99,
        },
    ]

    mock_calculer_occurrences.return_value = {
        "Max": 1,
        "Disney+": 2,
        "Netflix": 2,
        "Amazon": 1,
    }
    critere_service = CritereService()
    abonnement = critere_service.optimiser_abonnement(criteres)

    assert isinstance(abonnement, Abonnement)
    assert abonnement.nom_plateforme == "Max"
    assert abonnement.id_abonnement == 20
    mock_filtrer_abonnement.assert_called_once_with(criteres)
    mock_calculer_occurrences.assert_called_once_with(criteres)


@patch(
    "src.webservice.services.service_critere.CritereService.filtrer_abonnement"
)
@patch(
    "src.webservice.services.service_critere."
    "CritereService.calculer_occurrences_plateformes"
)
def test_optimiser_abonnement_rappoprt_prix(
    mock_calculer_occurrences,
    mock_filtrer_abonnement,
):
    # Préparer les données fictives
    criteres = Critere(
        1,
        {
            "qualite": "HD",
            "pub": True,
            "prix": False,
            "rapport_quantite_prix": True,
        },
    )

    mock_filtrer_abonnement.return_value = [
        {
            "id_abonnement": 14,
            "nom_plateforme": "Disney+",
            "prix": 10.99,
        },
        {
            "id_abonnement": 17,
            "nom_plateforme": "Netflix",
            "prix": 7.99,
        },
        {"id_abonnement": 20, "nom_plateforme": "Max", "prix": 5.99},
        {
            "id_abonnement": 1,
            "nom_plateforme": "Amazon",
            "prix": 6.99,
        },
    ]

    mock_calculer_occurrences.return_value = {
        "Max": 1,
        "Disney+": 2,
        "Netflix": 2,
        "Amazon": 1,
    }
    critere_service = CritereService()
    abonnement = critere_service.optimiser_abonnement(criteres)

    assert isinstance(abonnement, Abonnement)
    assert abonnement.nom_plateforme == "Netflix"
    assert abonnement.id_abonnement == 17
    mock_filtrer_abonnement.assert_called_once_with(criteres)
    mock_calculer_occurrences.assert_called_once_with(criteres)


@patch(
    "src.webservice.services.service_critere."
    "CritereService.optimiser_abonnement"
)
def test_afficher_abonnement(mock_optimiser_abonnement):
    critere_service = CritereService()
    abonnement_simule = Abonnement(
        id_abonnement=1,
        nom_plateforme="Amazon",
    )
    mock_optimiser_abonnement.return_value = abonnement_simule
    resultat = critere_service.afficher_abonnement_optimise(
        criteres=(1, {})
    )
    assert "Abonnement optimisé :" in resultat
    assert "Plateforme : Amazon" in resultat
    assert "ID de l'abonnement : 1" in resultat
    assert "Nom de l'abonnement : Avec pub" in resultat
    assert "Prix : 6.99 €" in resultat


@patch(
    "src.webservice.services.service_critere."
    "CritereService.optimiser_abonnement"
)
def test_afficher_abonnement_none(mock_optimiser_abonnement):
    critere_service = CritereService()
    mock_optimiser_abonnement.return_value = None
    resultat = critere_service.afficher_abonnement_optimise(
        criteres=(1, {})
    )
    assert resultat == "Aucun abonnement optimisé trouvé."
