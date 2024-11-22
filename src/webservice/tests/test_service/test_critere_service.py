from src.webservice.services.service_critere import CritereService
from src.webservice.business_object.critere import Critere
from src.webservice.business_object.abonnement import Abonnement
from src.webservice.business_object.watchlist import Watchlist
import pytest
from unittest.mock import patch, MagicMock


@patch("src.webservice.services.service_watchlist.WatchlistService.trouver_par_id")
@patch(
    "src.webservice.services.service_watchlist.WatchlistService.sauvegarder_watchlist"
)
@patch("src.webservice.business_object.film.Film.recuperer_streaming")
def test_recuperer_plateformes_film(
    mock_recuperer_streaming, mock_sauvegarder_watchlist, mock_trouver_par_id
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
            "logo": "https://image.tmdb.org/t/p/w780/eBXzkFEupZjKaIKY7zBUaSdCY8I.jpg",
        },
        {
            "id": 1899,
            "name": "Max",
            "logo": "https://image.tmdb.org/t/p/w780/fksCUZ9QDWZMUwL2LgMtLckROUN.jpg",
        },
    ]
    {268: ["Canal+", "Max"]}

    mock_trouver_par_id.return_value = watchlist_mock
    mock_sauvegarder_watchlist.return_value = films_mock
    mock_recuperer_streaming.return_value = plateformes_mock_101

    service = CritereService()
    resultat = service.recuperer_plateformes_film(critere)

    # Vérifications
    assert resultat == {268: ["Canal+", "Max"]}

    # Vérifie les appels des mocks
    mock_trouver_par_id.assert_called_once_with(id_watchlist)
    mock_sauvegarder_watchlist.assert_called_once_with(watchlist_mock)


@patch("src.webservice.dao.abonnement_dao.AbonnementDao.abonnement_filtrés")
def test_filtrer_abonnement(mock_abonnement_filtrees):
    criteres = Critere(
        1, {"qualite": "4K", "pub": True, "prix": False, "rapport_quantite_prix": False}
    )
    abonnement_mock = [{"id_abonnement": 1, "nom_plateforme": "Amazon", "prix": "6.99"}]
    mock_abonnement_filtrees.return_value = abonnement_mock
    service = CritereService()
    resultat = service.filtrer_abonnement(criteres)
    assert resultat == abonnement_mock


@patch("src.webservice.services.service_critere.CritereService.filtrer_abonnement")
@patch(
    "src.webservice.services.service_critere.CritereService.recuperer_plateformes_film"
)
def test_calculer_occurrences_plateformes(
    mock_recuperer_plateformes_film, mock_filtrer_abonnement
):
    criteres = Critere(
        1, {"qualite": "HD", "pub": True, "prix": False, "rapport_quantite_prix": False}
    )

    mock_filtrer_abonnement.return_value = [
        {"id_abonnement": 14, "nom_plateforme": "Disney+", "prix": "5.99"},
        {"id_abonnement": 17, "nom_plateforme": "Netflix", "prix": "5.99"},
        {"id_abonnement": 20, "nom_plateforme": "Max", "prix": "5.99"},
        {"id_abonnement": 1, "nom_plateforme": "Amazon", "prix": "6.99"},
    ]
    mock_recuperer_plateformes_film.return_value = {268: ["Canal+", "Max"]}

    critere_service = CritereService()

    # Appel de la méthode à tester
    occurrences = critere_service.calculer_occurrences_plateformes(criteres)

    # Assertions
    assert occurrences == {"Max": 1}
    mock_filtrer_abonnement.assert_called_once_with(criteres)
    mock_recuperer_plateformes_film.assert_called_once_with(criteres)


@patch("src.webservice.services.service_critere.CritereService.filtrer_abonnement")
@patch(
    "src.webservice.services.service_critere.CritereService.recuperer_plateformes_film"
)
@patch(
    "src.webservice.services.service_critere.CritereService.calculer_occurrences_plateformes"
)
def test_optimiser_abonnement_nb_films(
    mock_calculer_occurrences, mock_recuperer_plateformes, mock_filtrer_abonnement
):
    # Préparer les données fictives
    criteres = Critere(
        1, {"qualite": "HD", "pub": True, "prix": False, "rapport_quantite_prix": False}
    )

    mock_filtrer_abonnement.return_value = [
        {"id_abonnement": 14, "nom_plateforme": "Disney+", "prix": 5.99},
        {"id_abonnement": 17, "nom_plateforme": "Netflix", "prix": 5.99},
        {"id_abonnement": 20, "nom_plateforme": "Max", "prix": 5.99},
        {"id_abonnement": 1, "nom_plateforme": "Amazon", "prix": 6.99},
    ]
    mock_recuperer_plateformes.return_value = {
        268: ["Canal+", "Max", "Disney+", "Netflix"],
        152: [
            "Canal+",
            "Disney+",
            "Amazon",
            "Paramount Plus Apple TV Channel ",
            "Netflix",
        ],
    }

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
    mock_recuperer_plateformes.assert_called_once_with(criteres)
    mock_calculer_occurrences.assert_called_once_with(criteres)


@patch("src.webservice.services.service_critere.CritereService.filtrer_abonnement")
@patch(
    "src.webservice.services.service_critere.CritereService.recuperer_plateformes_film"
)
@patch(
    "src.webservice.services.service_critere.CritereService.calculer_occurrences_plateformes"
)
def test_optimiser_abonnement_prix(
    mock_calculer_occurrences, mock_recuperer_plateformes, mock_filtrer_abonnement
):
    # Préparer les données fictives
    criteres = Critere(
        1, {"qualite": "HD", "pub": True, "prix": True, "rapport_quantite_prix": False}
    )

    mock_filtrer_abonnement.return_value = [
        {"id_abonnement": 14, "nom_plateforme": "Disney+", "prix": 10.99},
        {"id_abonnement": 17, "nom_plateforme": "Netflix", "prix": 7.99},
        {"id_abonnement": 20, "nom_plateforme": "Max", "prix": 5.99},
        {"id_abonnement": 1, "nom_plateforme": "Amazon", "prix": 6.99},
    ]
    mock_recuperer_plateformes.return_value = {
        268: ["Canal+", "Max", "Disney+", "Netflix"],
        152: [
            "Canal+",
            "Disney+",
            "Amazon",
            "Paramount Plus Apple TV Channel ",
            "Netflix",
        ],
    }

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
    mock_recuperer_plateformes.assert_called_once_with(criteres)
    mock_calculer_occurrences.assert_called_once_with(criteres)


@patch("src.webservice.services.service_critere.CritereService.filtrer_abonnement")
@patch(
    "src.webservice.services.service_critere.CritereService.recuperer_plateformes_film"
)
@patch(
    "src.webservice.services.service_critere.CritereService.calculer_occurrences_plateformes"
)
def test_optimiser_abonnement_rappoprt_prix(
    mock_calculer_occurrences, mock_recuperer_plateformes, mock_filtrer_abonnement
):
    # Préparer les données fictives
    criteres = Critere(
        1, {"qualite": "HD", "pub": True, "prix": False, "rapport_quantite_prix": True}
    )

    mock_filtrer_abonnement.return_value = [
        {"id_abonnement": 14, "nom_plateforme": "Disney+", "prix": 10.99},
        {"id_abonnement": 17, "nom_plateforme": "Netflix", "prix": 7.99},
        {"id_abonnement": 20, "nom_plateforme": "Max", "prix": 5.99},
        {"id_abonnement": 1, "nom_plateforme": "Amazon", "prix": 6.99},
    ]
    mock_recuperer_plateformes.return_value = {
        268: ["Canal+", "Max", "Disney+", "Netflix"],
        152: [
            "Canal+",
            "Disney+",
            "Amazon",
            "Paramount Plus Apple TV Channel ",
            "Netflix",
        ],
    }

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
    mock_recuperer_plateformes.assert_called_once_with(criteres)
    mock_calculer_occurrences.assert_called_once_with(criteres)


"""
if __name__ == "__main__":
    creationu = UtilisateurService().creer_compte(
        nom="Alice",
        prenom="Dupont",
        pseudo="alice123",
        adresse_mail="alice@example.com",
        mdp="password123",
        langue="français",
    )

    creation1 = WatchlistService().creer_nouvelle_watchlist("favories", creationu)
    # creation2 = WatchlistService().creer_nouvelle_watchlist("favories2" ,creationu)
    film = Film(268)
    film2 = Film(152)
    #print(film.recuperer_streaming())
    ajoutfilm = WatchlistService().ajouter_film(film, creation1)
    ajoutfilm2 = WatchlistService().ajouter_film(film2, creation1)
    criteres = Critere(1, {"qualite":"HD", "pub":True, "prix":False,'rapport_quantite_prix':False})
    #plateforme = CritereService().recuperer_plateformes_film(criteres)
    #print(plateforme)
    #print(plateforme)
    #filtres = CritereService().filtrer_abonnement(criteres)
    #print(filtres)
    #print(filtres)
    occurences = CritereService().calculer_occurrences_plateformes(criteres)
    print(occurences)
    #optimisation = CritereService().optimiser_abonnement(criteres)
    #print(optimisation)
    #print( CritereService().afficher_abonnement_optimise(criteres))"""
