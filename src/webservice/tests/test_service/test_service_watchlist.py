from unittest.mock import patch
import pytest
from src.webservice.services.service_watchlist import WatchlistService
from src.webservice.business_object.watchlist import Watchlist
from src.webservice.business_object.utilisateur import Utilisateur
from src.webservice.business_object.film import Film


@patch("src.webservice.dao.watchlist_dao.WatchlistDao.creer_nouvelle_watchlist_DAO")
def test_creer_nouvelle_watchlist_succes(mock_creer_watchlist):
    """
    Test de la création d'une nouvelle watchlist avec succès.
    """
    service = WatchlistService()

    utilisateur = Utilisateur(
        id_utilisateur=1,
        nom="TestNom",
        prenom="TestPrenom",
        pseudo="TestUser",
        adresse_mail="test@example.com",
        mdp="hashed_password",
    )
    nom_watchlist = "Ma Watchlist"
    mock_creer_watchlist.return_value = (
        True  # Simule un succès lors de la création en DB
    )

    # Appeler la méthode
    result = service.creer_nouvelle_watchlist(nom_watchlist, utilisateur)

    # Vérifier que la watchlist est créée correctement
    assert isinstance(result, Watchlist)
    assert result.nom_watchlist == nom_watchlist
    assert result.id_utilisateur == utilisateur.id_utilisateur


@patch("src.webservice.dao.watchlist_dao.WatchlistDao.creer_nouvelle_watchlist_DAO")
def test_creer_nouvelle_watchlist_echec(mock_creer_watchlist):
    """
    Test de l'échec de la création d'une nouvelle watchlist.
    """
    service = WatchlistService()

    utilisateur = Utilisateur(
        id_utilisateur=1,
        nom="TestNom",
        prenom="TestPrenom",
        pseudo="TestUser",
        adresse_mail="test@example.com",
        mdp="hashed_password",
    )
    nom_watchlist = "Ma Watchlist"
    mock_creer_watchlist.return_value = False

    # Appeler la méthode
    result = service.creer_nouvelle_watchlist(nom_watchlist, utilisateur)

    assert result is None


@patch("src.webservice.dao.watchlist_dao.WatchlistDao.creer_nouvelle_watchlist_DAO")
def test_creer_nouvelle_watchlist_nom_watchlist_none(mock_creer_watchlist):
    """
    Test de la création d'une watchlist avec un nom de watchlist égal à None.
    """
    service = WatchlistService()

    # Création d'un utilisateur valide
    utilisateur_valid = Utilisateur(
        id_utilisateur=1,
        nom="TestNom",
        prenom="TestPrenom",
        pseudo="TestUser",
        adresse_mail="test@example.com",
        mdp="hashed_password",
    )

    # Appeler la méthode avec nom_watchlist = None
    result = service.creer_nouvelle_watchlist(None, utilisateur_valid)

    # Vérifications
    assert result is None  # La méthode doit retourner None pour un nom invalide
    mock_creer_watchlist.assert_not_called()


@patch("src.webservice.dao.watchlist_dao.WatchlistDao.supprimer_watchlist_DAO")
def test_supprimer_watchlist_succes(mock_supprimer_watchlist):
    """
    Test de la suppression d'une watchlist avec succès.
    """
    service = WatchlistService()

    # Mock de la méthode DAO pour renvoyer True (suppression réussie)
    mock_supprimer_watchlist.return_value = True

    # Création d'une watchlist valide
    watchlist_valid = Watchlist(
        id_watchlist=1, nom_watchlist="MaWatchlist", id_utilisateur=1
    )

    # Appeler la méthode de suppression
    result = service.supprimer_watchlist(watchlist_valid)

    # Vérifications
    assert result is True  # La suppression doit réussir
    mock_supprimer_watchlist.assert_called_once_with(watchlist_valid)


@patch("src.webservice.dao.watchlist_dao.WatchlistDao.supprimer_watchlist_DAO")
def test_supprimer_watchlist_echec(mock_supprimer_watchlist):
    """
    Test de l'échec de la suppression d'une watchlist.
    """
    service = WatchlistService()

    # Mock de la méthode DAO pour renvoyer False (échec de suppression)
    mock_supprimer_watchlist.return_value = False

    # Création d'une watchlist valide
    watchlist_valid = Watchlist(
        id_watchlist=2, nom_watchlist="AutreWatchlist", id_utilisateur=1
    )

    # Appeler la méthode de suppression
    result = service.supprimer_watchlist(watchlist_valid)

    # Vérifications
    assert result is False  # La suppression doit échouer
    mock_supprimer_watchlist.assert_called_once_with(watchlist_valid)


@patch("src.webservice.dao.watchlist_dao.WatchlistDao.ajouter_film_DAO")
@patch("src.webservice.dao.watchlist_dao.WatchlistDao.verifier_film_existe")
@patch("src.webservice.dao.watchlist_dao.WatchlistDao.film_deja_present")
def test_ajouter_film_succes(
    mock_film_deja_present, mock_verifier_film_existe, mock_ajouter_film_DAO
):
    """
    Test de l'ajout d'un film avec succès.
    """
    service = WatchlistService()

    # Création d'un film et d'une watchlist
    film = Film(id_film=1)
    watchlist = Watchlist(
        id_watchlist=1, nom_watchlist="Ma Watchlist", id_utilisateur=1
    )

    # Configurer les mocks pour simuler un ajout réussi
    mock_film_deja_present.return_value = False
    mock_verifier_film_existe.return_value = True
    mock_ajouter_film_DAO.return_value = True

    # Appeler la méthode
    resultat = service.ajouter_film(film, watchlist)

    # Vérifications
    assert resultat is True  # L'ajout doit réussir
    mock_film_deja_present.assert_called_once_with(watchlist.id_watchlist, film.id_film)
    mock_verifier_film_existe.assert_called_once_with(film.id_film)
    mock_ajouter_film_DAO.assert_called_once_with(watchlist.id_watchlist, film.id_film)


@patch("src.webservice.dao.watchlist_dao.WatchlistDao.film_deja_present")
def test_ajouter_film_deja_present(mock_film_deja_present):
    """
    Test de l'ajout d'un film déjà présent dans la watchlist.
    """
    service = WatchlistService()

    # Création d'un film et d'une watchlist
    film = Film(id_film=1)
    watchlist = Watchlist(
        id_watchlist=1, nom_watchlist="Ma Watchlist", id_utilisateur=1
    )

    # Configurer le mock pour indiquer que le film est déjà présent
    mock_film_deja_present.return_value = True

    # Appeler la méthode
    resultat = service.ajouter_film(film, watchlist)

    # Vérifications
    assert resultat is False  # L'ajout doit échouer
    mock_film_deja_present.assert_called_once_with(watchlist.id_watchlist, film.id_film)


@patch("src.webservice.dao.film_dao.FilmDao.ajouter_film")
@patch("src.webservice.dao.watchlist_dao.WatchlistDao.verifier_film_existe")
@patch("src.webservice.dao.watchlist_dao.WatchlistDao.ajouter_film_DAO")
@patch("src.webservice.dao.watchlist_dao.WatchlistDao.film_deja_present")
def test_ajouter_film_inexistant_ajoute_succes(
    mock_film_deja_present,
    mock_ajouter_film,
    mock_verifier_film_existe,
    mock_ajouter_film_DAO,
):
    """
    Test de l'ajout d'un film inexistant dans la base, mais ajouté avec succès.
    """
    service = WatchlistService()

    # Création d'un film et d'une watchlist
    film = Film(id_film=1)
    watchlist = Watchlist(
        id_watchlist=1, nom_watchlist="Ma Watchlist", id_utilisateur=1
    )

    # Configurer les mocks
    mock_film_deja_present.return_value = False
    mock_verifier_film_existe.return_value = False
    mock_ajouter_film.return_value = True
    mock_ajouter_film_DAO.return_value = True

    # Appeler la méthode
    resultat = service.ajouter_film(film, watchlist)

    # Vérifications
    assert resultat is True


@patch("src.webservice.dao.watchlist_dao.WatchlistDao.ajouter_film_DAO")
@patch("src.webservice.dao.watchlist_dao.WatchlistDao.verifier_film_existe")
@patch("src.webservice.dao.watchlist_dao.WatchlistDao.film_deja_present")
def test_ajouter_film_echec(
    mock_film_deja_present, mock_verifier_film_existe, mock_ajouter_film_DAO
):
    """
    Test de l'échec de l'ajout d'un film dans la watchlist.
    """
    service = WatchlistService()

    # Création d'un film et d'une watchlist
    film = Film(id_film=1)
    watchlist = Watchlist(
        id_watchlist=1, nom_watchlist="Ma Watchlist", id_utilisateur=1
    )

    # Configurer les mocks pour simuler un échec
    mock_film_deja_present.return_value = False
    mock_verifier_film_existe.return_value = True
    mock_ajouter_film_DAO.return_value = False

    # Appeler la méthode
    resultat = service.ajouter_film(film, watchlist)

    # Vérifications
    assert resultat is False


@patch("src.webservice.dao.watchlist_dao.WatchlistDao.film_deja_present")
@patch("src.webservice.dao.watchlist_dao.WatchlistDao.supprimer_film_DAO")
def test_supprimer_film_succes(mock_supprimer_film_DAO, mock_film_deja_present):
    # Initialisation
    service = WatchlistService()
    film = Film(id_film=1)
    watchlist = Watchlist(
        id_watchlist=1, nom_watchlist="Test Watchlist", id_utilisateur=1
    )

    # Cas succès de la suppression
    mock_film_deja_present.return_value = True
    mock_supprimer_film_DAO.return_value = True

    resultat = service.supprimer_film(film, watchlist)

    assert resultat is True


@patch("src.webservice.dao.watchlist_dao.WatchlistDao.film_deja_present")
def test_supprimer_film_non_present(mock_film_deja_present):
    # Initialisation
    service = WatchlistService()
    film = Film(id_film=1)
    watchlist = Watchlist(
        id_watchlist=1, nom_watchlist="Test Watchlist", id_utilisateur=1
    )
    mock_film_deja_present.return_value = False

    resultat = service.supprimer_film(film, watchlist)

    assert resultat is False


@patch("src.webservice.dao.watchlist_dao.WatchlistDao.film_deja_present")
@patch("src.webservice.dao.watchlist_dao.WatchlistDao.supprimer_film_DAO")
def test_supprimer_film_echec(mock_supprimer_film_DAO, mock_film_deja_present):
    # Initialisation
    service = WatchlistService()
    film = Film(id_film=1)
    watchlist = Watchlist(
        id_watchlist=1, nom_watchlist="Test Watchlist", id_utilisateur=1
    )

    # Cas échec de la suppression
    mock_film_deja_present.return_value = True
    mock_supprimer_film_DAO.return_value = False

    resultat = service.supprimer_film(film, watchlist)

    assert resultat is False


@patch("src.webservice.dao.watchlist_dao.WatchlistDao.recuperer_films_watchlist_DAO")
def test_sauvegarder_watchlist_succes(mock_recuperer_films):
    # Initialisation
    service = WatchlistService()
    watchlist = Watchlist(
        id_watchlist=1, nom_watchlist="Test Watchlist", id_utilisateur=1
    )

    # Simuler une liste de films retournée
    mock_recuperer_films.return_value = [Film(id_film=1), Film(id_film=2)]

    resultat = service.sauvegarder_watchlist(watchlist)

    assert resultat == mock_recuperer_films.return_value
    assert watchlist.list_film == mock_recuperer_films.return_value
    mock_recuperer_films.assert_called_once_with(1)


@patch("src.webservice.dao.watchlist_dao.WatchlistDao.recuperer_films_watchlist_DAO")
def test_sauvegarder_watchlist_succes(mock_recuperer_films):
    # Initialisation
    service = WatchlistService()
    watchlist = Watchlist(
        id_watchlist=1, nom_watchlist="Test Watchlist", id_utilisateur=1
    )

    # Simuler une liste de films retournée
    mock_recuperer_films.return_value = [Film(id_film=1), Film(id_film=2)]

    resultat = service.sauvegarder_watchlist(watchlist)

    assert resultat == mock_recuperer_films.return_value
    assert watchlist.list_film == mock_recuperer_films.return_value
    mock_recuperer_films.assert_called_once_with(1)


def test_sauvegarder_watchlist_id_invalide():
    # Initialisation
    service = WatchlistService()
    watchlist = Watchlist(
        id_watchlist=None, nom_watchlist="Test Watchlist", id_utilisateur=1
    )

    # Cas d'erreur : watchlist sans ID valide
    with patch("logging.error") as mock_logging_error:
        resultat = service.sauvegarder_watchlist(watchlist)

    assert resultat == []
    mock_logging_error.assert_called_once_with(
        "Erreur: l'identifiant de la watchlist est invalide ou manquant."
    )


@patch("src.webservice.dao.watchlist_dao.WatchlistDao.recuperer_films_watchlist_DAO")
def test_sauvegarder_watchlist_aucun_film(mock_recuperer_films):
    # Initialisation
    service = WatchlistService()
    watchlist = Watchlist(
        id_watchlist=1, nom_watchlist="Test Watchlist", id_utilisateur=1
    )

    # Simuler une watchlist vide
    mock_recuperer_films.return_value = []

    resultat = service.sauvegarder_watchlist(watchlist)

    assert resultat == []
    assert watchlist.list_film == []
    mock_recuperer_films.assert_called_once_with(1)


@patch("src.webservice.dao.watchlist_dao.WatchlistDao.afficher_watchlist_DAO")
@patch(
    "src.webservice.services.service_watchlist.WatchlistService.sauvegarder_watchlist"
)
def test_afficher_watchlist_succes(mock_sauvegarder_watchlist, mock_afficher_watchlist):
    service = WatchlistService()
    id_utilisateur = 1
    mock_afficher_watchlist.return_value = [
        {"id_watchlist": 1, "nom_watchlist": "favories"}
    ]
    mock_sauvegarder_watchlist.return_value = [
        {"id_film": 268, "nom_film": "Batman"},
        {"id_film": 152, "nom_film": "Star Trek: The Motion Picture"},
    ]
    result = service.afficher_watchlist(id_utilisateur)
    expected_watchlist = [
        {
            "id_watchlist": 1,
            "nom_watchlist": "favories",
            "films": [
                {"id_film": 268, "nom_film": "Batman"},
                {"id_film": 152, "nom_film": "Star Trek: The Motion Picture"},
            ],
        }
    ]
    assert result == expected_watchlist


@patch("src.webservice.dao.watchlist_dao.WatchlistDao.trouver_par_id_w")
@patch(
    "src.webservice.services.service_watchlist.WatchlistService.sauvegarder_watchlist"
)
def trouver_par_id(mock_sauvegarder_watchlist, mock_trouver_par_id_w):
    id_watchlist = 2
    mock_trouver_par_id_w.return_value = Watchlist("test", 1, [], id_watchlist)
    mock_sauvegarder_watchlist.return_value = [{"id_film": 1, "nom_film": "Film Test"}]
    service = WatchlistService()
    result = service.trouver_par_id(id_watchlist)
    assert result.nom_watchlist == "test"
    assert result.id_watchlist == 2
    assert result.id_utilisateur == 1
    assert result.list_film == [{"id_film": 1, "nom_film": "Film Test"}]
