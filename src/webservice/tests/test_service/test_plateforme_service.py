import pytest
from unittest.mock import MagicMock, patch
from src.webservice.business_object.film import Film
from src.webservice.services.service_plateforme import (
    ServicePlateforme,
)


@patch(
    "src.webservice.dao.plateforme_dao.PlateformeDAO."
    "verifier_plateforme_existe"
)
@patch(
    "src.webservice.dao.plateforme_dao.PlateformeDAO."
    "ajouter_plateforme"
)
def test_mettre_a_jour_plateforme_plateforme_non_existante(
    mock_ajouter_plateforme, mock_verifier_plateforme_existe
):
    # Test lorsque la plateforme n'existe pas encore
    mock_verifier_plateforme_existe.return_value = False
    mock_ajouter_plateforme.return_value = True

    service = ServicePlateforme()
    resultat = service.mettre_a_jour_plateforme("Netflix", 1)

    assert resultat is True
    mock_verifier_plateforme_existe.assert_called_with(1, "Netflix")
    mock_ajouter_plateforme.assert_called_once()


@patch(
    "src.webservice.dao.plateforme_dao.PlateformeDAO."
    "verifier_plateforme_existe"
)
def test_mettre_a_jour_plateforme_plateforme_existante(
    mock_verifier_plateforme_existe,
):
    # Test lorsque la plateforme existe déjà
    mock_verifier_plateforme_existe.return_value = True

    service = ServicePlateforme()
    resultat = service.mettre_a_jour_plateforme("Netflix", 1)

    assert resultat is False
    mock_verifier_plateforme_existe.assert_called_with(1, "Netflix")


@patch(
    "src.webservice.dao.plateforme_dao.PlateformeDAO."
    "verifier_plateforme_existe"
)
@patch(
    "src.webservice.dao.plateforme_dao.PlateformeDAO.ajouter_plateforme"
)
def test_mettre_a_jour_plateforme_exception(
    mock_ajouter_plateforme, mock_verifier_plateforme_existe
):
    # Test lorsqu'une exception est levée
    mock_verifier_plateforme_existe.side_effect = Exception(
        "Erreur de base de données"
    )

    service = ServicePlateforme()
    resultat = service.mettre_a_jour_plateforme("Netflix", 1)

    assert resultat is False
    mock_verifier_plateforme_existe.assert_called_with(1, "Netflix")


@patch("src.webservice.business_object.film.Film.recuperer_streaming")
def test_ajouter_plateforme_sans_platforme(mock_recuperer_streaming):
    # Test lorsque le film ne retourne aucune plateforme
    film_mock = MagicMock(spec=Film)
    film_mock.id_film = 123
    mock_recuperer_streaming.return_value = []

    service = ServicePlateforme()
    service.mettre_a_jour_plateforme = MagicMock(return_value=True)

    service.ajouter_plateforme(film_mock)

    service.mettre_a_jour_plateforme.assert_not_called()


@pytest.fixture
def mock_service_plateforme():
    return ServicePlateforme()


@pytest.fixture
def mock_film():
    return Film(268)


@pytest.fixture
def mock_recuperer_streaming():
    with patch(
        "src.webservice.business_object.film.Film.recuperer_streaming"
    ) as mock:
        yield mock


@pytest.fixture
def mock_mettre_a_jour_plateforme():
    with patch(
        "src.webservice.services.service_plateforme."
        "ServicePlateforme.mettre_a_jour_plateforme"
    ) as mock:
        yield mock


@pytest.fixture
def mock_ajouter_relation_film_plateforme():
    with patch(
        "src.webservice.dao.plateforme_dao.PlateformeDAO."
        "ajouter_relation_film_plateforme"
    ) as mock:
        yield mock


def test_ajouter_plateforme_success(
    mock_film,
    mock_recuperer_streaming,
    mock_mettre_a_jour_plateforme,
    mock_service_plateforme,
    mock_ajouter_relation_film_plateforme,
):
    mock_recuperer_streaming.return_value = [
        {
            "id": 381,
            "name": "Canal+",
            "logo": "https://image.tmdb.org/t/p/"
            "w780/eBXzkFEupZjKaIKY7zBUaSdCY8I.jpg",
        },
        {
            "id": 1899,
            "name": "Max",
            "logo": "https://image.tmdb.org/t/"
            "p/w780/fksCUZ9QDWZMUwL2LgMtLckROUN.jpg",
        },
    ]
    mock_mettre_a_jour_plateforme.return_value = True

    mock_service_plateforme.ajouter_plateforme(mock_film)
