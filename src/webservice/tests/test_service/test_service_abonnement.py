import pytest
from unittest.mock import patch
from src.webservice.dao.abonnement_dao import AbonnementDao
from src.webservice.services.service_abonnement import (
    AbonnementService,
)


@pytest.fixture
def abonnement_service():
    return AbonnementService()


@patch.object(AbonnementDao, "get_prix_abonnement_DAO")
def test_prix_abonnement(mock_get_prix_abonnement_DAO):
    # Configuration du mock
    mock_get_prix_abonnement_DAO.return_value = 10.99
    service = AbonnementService()
    prix = service.prix_abonnement(1)

    # Vérification
    assert prix == 10.99


@patch.object(AbonnementDao, "get_pub_abonnement_DAO")
def test_pub_abonnement_avec_pub(mock_get_pub_abonnement_DAO):
    # Configuration du mock pour retour de pub
    mock_get_pub_abonnement_DAO.return_value = True
    service = AbonnementService()

    # Appel de la méthode à tester
    pub = service.pub_abonnement(1)
    assert pub == "Cet abonnement contient des pub !"


@patch.object(AbonnementDao, "get_pub_abonnement_DAO")
def test_pub_abonnement_sans_pub(mock_get_pub_abonnement_DAO):
    # Configuration du mock pour pas de pub
    mock_get_pub_abonnement_DAO.return_value = False
    service = AbonnementService()

    # Appel de la méthode à tester
    pub = service.pub_abonnement(1)

    # Vérification
    assert pub == "Cet abonnement ne contient pas des pub !"


@patch.object(AbonnementDao, "get_qualite_abonnement_DAO")
def test_qualite_abonnement(mock_get_qualite_abonnement_DAO):
    # Configuration du mock pour la qualité
    mock_get_qualite_abonnement_DAO.return_value = "HD"
    service = AbonnementService()

    # Appel de la méthode à tester
    qualite = service.qualite_abonnement(1)

    # Vérification
    assert qualite == "HD"


@patch.object(AbonnementDao, "get_nom_abonnement_DAO")
def test_recherche_abonnement(mock_get_nom_abonnement_DAO):
    # Configuration du mock pour la liste d'abonnements
    mock_get_nom_abonnement_DAO.return_value = [
        "Abonnement 1",
        "Abonnement 2",
    ]
    service = AbonnementService()

    # Appel de la méthode à tester
    abonnement_list = service.recherche_abonnement("Netflix", 1)

    # Vérification
    assert abonnement_list == ["Abonnement 1", "Abonnement 2"]
