import pytest
from unittest.mock import patch, MagicMock
from src.webservice.business_object.utilisateur import Utilisateur
from src.webservice.utils.securite import hash_mdp
from src.webservice.services.service_utilisateur import UtilisateurService

@pytest.fixture
def utilisateur_service():
    """
    Fixture pour créer une instance de UtilisateurService pour les tests.
    """
    utilisateur = Utilisateur(
        id_utilisateur=1,
        nom="TestNom",
        prenom="TestPrenom",
        pseudo="TestPseudo",
        adresse_mail="test@test.com",
        mdp="hashed_password",
        langue="français",
        sel="test_sel"
    )
    return UtilisateurService(utilisateur)


@patch('src.webservice.dao.utilisateur_dao.UtilisateurDAO.creer_compte_DAO')
def test_creer_compte_succes(mock_creer_compte, utilisateur_service):
    """
    Test pour vérifier la création d'un compte utilisateur avec succès.
    """
    mock_creer_compte.return_value = 1

    utilisateur = utilisateur_service.creer_compte(
        nom="TestNom",
        prenom="TestPrenom",
        pseudo="TestPseudo",
        adresse_mail="test@test.com",
        mdp="test_mdp",
        langue="français"
    )

    assert utilisateur.id_utilisateur == 1
    assert utilisateur.nom == "TestNom"
    assert utilisateur.pseudo == "TestPseudo"


@patch('src.webservice.dao.utilisateur_dao.UtilisateurDAO.creer_compte_DAO')
def test_creer_compte_echec(mock_creer_compte, utilisateur_service):
    """
    Test pour vérifier l'échec de la création d'un compte utilisateur (pseudo déjà utilisé).
    """
    mock_creer_compte.return_value = None

    with pytest.raises(ValueError, match="Erreur lors de la création du compte"):
        utilisateur_service.creer_compte(
            nom="TestNom",
            prenom="TestPrenom",
            pseudo="TestPseudo",
            adresse_mail="test@test.com",
            mdp="test_mdp",
            langue="français"
        )


@patch('src.webservice.dao.utilisateur_dao.UtilisateurDAO.supprimer_compte_DAO')
def test_supprimer_compte_succes(mock_supprimer_compte, utilisateur_service):
    """
    Test pour vérifier la suppression d'un compte utilisateur avec succès.
    """
    mock_supprimer_compte.return_value = True

    try:
        utilisateur_service.supprimer_compte(id_utilisateur=1)
    except ValueError:
        pytest.fail("Suppression d'utilisateur a levé une exception imprévue.")


@patch('src.webservice.dao.utilisateur_dao.UtilisateurDAO.supprimer_compte_DAO')
def test_supprimer_compte_echec(mock_supprimer_compte, utilisateur_service):
    """
    Test pour vérifier l'échec de la suppression d'un compte utilisateur (utilisateur introuvable).
    """
    mock_supprimer_compte.return_value = False

    with pytest.raises(ValueError, match="Utilisateur introuvable ou suppression échouée"):
        utilisateur_service.supprimer_compte(id_utilisateur=1)


@patch('src.webservice.dao.utilisateur_dao.UtilisateurDAO.se_connecter_DAO')
def test_se_connecter_succes(mock_se_connecter, utilisateur_service):
    """
    Test pour vérifier la connexion d'un utilisateur avec succès.
    """
    # Hash un mot de passe test pour correspondre
    hashed_mdp, sel = hash_mdp("test_mdp")

    mock_se_connecter.return_value = {
        "id_utilisateur": 1,
        "nom": "TestNom",
        "prenom": "TestPrenom",
        "pseudo": "TestPseudo",
        "adresse_mail": "test@test.com",
        "mdp": hashed_mdp,
        "langue": "français",
        "sel": sel
    }

    message = utilisateur_service.se_connecter(pseudo="TestPseudo", mdp="test_mdp")
    assert message == "Bienvenue TestPseudo sur notre application"


@patch('src.webservice.dao.utilisateur_dao.UtilisateurDAO.se_connecter_DAO')
def test_se_connecter_echec(mock_se_connecter, utilisateur_service):
    """
    Test pour vérifier l'échec de la connexion d'un utilisateur (mot de passe incorrect).
    """
    # Hash un mot de passe test différent pour simuler un mauvais mot de passe
    hashed_mdp, sel = hash_mdp("wrong_mdp")

    mock_se_connecter.return_value = {
        "id_utilisateur": 1,
        "nom": "TestNom",
        "prenom": "TestPrenom",
        "pseudo": "TestPseudo",
        "adresse_mail": "test@test.com",
        "mdp": hashed_mdp,
        "langue": "français",
        "sel": sel
    }

    with pytest.raises(ValueError, match="Pseudo ou mot de passe incorrect"):
        utilisateur_service.se_connecter(pseudo="TestPseudo", mdp="test_mdp")


@patch('src.webservice.dao.utilisateur_dao.UtilisateurDAO.trouver_par_id')
def test_afficher_succes(mock_trouver_par_id, utilisateur_service):
    """
    Test pour vérifier l'affichage des informations d'un utilisateur avec succès.
    """
    mock_trouver_par_id.return_value = Utilisateur(
        id_utilisateur=1,
        nom="TestNom",
        prenom="TestPrenom",
        pseudo="TestPseudo",
        adresse_mail="test@test.com",
        mdp="hashed_password",
        langue="français",
        sel="test_sel"
    )

    utilisateur_info = utilisateur_service.afficher(id_utilisateur=1)
    assert utilisateur_info["Nom"] == "TestNom"
    assert utilisateur_info["Pseudo"] == "TestPseudo"


@patch('src.webservice.dao.utilisateur_dao.UtilisateurDAO.trouver_par_id')
def test_afficher_echec(mock_trouver_par_id, utilisateur_service):
    """
    Test pour vérifier l'échec de l'affichage des informations d'un utilisateur (utilisateur introuvable).
    """
    mock_trouver_par_id.return_value = None

    with pytest.raises(ValueError, match="Utilisateur introuvable"):
        utilisateur_service.afficher(id_utilisateur=1)
