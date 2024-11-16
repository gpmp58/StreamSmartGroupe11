import pytest
from unittest.mock import patch, MagicMock
from src.webservice.business_object.utilisateur import Utilisateur
from src.webservice.utils.securite import hash_mdp
from src.webservice.services.service_utilisateur import UtilisateurService

@pytest.fixture
def utilisateur_service():
    return UtilisateurService()

def test_creer_compte_succes(utilisateur_service):
    with patch("src.webservice.dao.utilisateur_dao.UtilisateurDAO.creer_compte_DAO", return_value=1) as mock_dao, \
         patch.object(utilisateur_service, "verifier_pseudo", return_value=False) as mock_verifier_pseudo:
        
        utilisateur = utilisateur_service.creer_compte(
            nom="Test",
            prenom="Test1",
            pseudo="test12",
            adresse_mail="test@example.com",
            mdp="password123",
            langue="français"
        )
        # Assertions
        mock_verifier_pseudo.assert_called_once_with("test12")
        assert isinstance(utilisateur, Utilisateur)
        assert utilisateur.nom == "Test"
        assert utilisateur.pseudo == "test12"

def test_creer_compte_pseudo_existant(utilisateur_service):
    with patch.object(utilisateur_service, "verifier_pseudo", return_value=True):
        with pytest.raises(ValueError, match="Le pseudo est déjà utilisé. Veuillez en choisir un autre."):
            utilisateur_service.creer_compte(
                nom="Test",
                prenom="Test1",
                pseudo="test12",
                adresse_mail="test@example.com",
                mdp="password123",
            )
def test_creer_compte_echec_creation(utilisateur_service):
    with patch("src.webservice.utils.securite.hash_mdp", return_value=("hashed_mdp", "sel")), \
         patch("src.webservice.dao.utilisateur_dao.UtilisateurDAO.creer_compte_DAO", return_value=None), \
         patch.object(utilisateur_service, "verifier_pseudo", return_value=False):
        
        with pytest.raises(ValueError, match="Erreur lors de la création du compte."):
            utilisateur_service.creer_compte(
                nom="Test",
                prenom="Test1",
                pseudo="test12",
                adresse_mail="test@example.com",
                mdp="password123",
            )
def test_supprimer_compte_succes():
    """
    Test de la suppression réussie d'un compte utilisateur.
    """
    utilisateur_service = UtilisateurService()
    with patch("src.webservice.dao.utilisateur_dao.UtilisateurDAO.supprimer_compte_DAO", return_value=True) as mock_supprimer:
        utilisateur_service.supprimer_compte(1)
        mock_supprimer.assert_called_once_with(1)
def test_supprimer_compte_utilisateur_introuvable():
    """
    Test de la suppression d'un compte inexistant.
    """
    utilisateur_service = UtilisateurService()
    with patch("src.webservice.dao.utilisateur_dao.UtilisateurDAO.supprimer_compte_DAO", return_value=False) as mock_supprimer:
        with pytest.raises(ValueError, match="Utilisateur introuvable ou suppression échouée."):
            utilisateur_service.supprimer_compte(999)  # ID inexistant
        mock_supprimer.assert_called_once_with(999)

def test_supprimer_compte_exception():
    """
    Test de la gestion des exceptions lors de la suppression.
    """
    utilisateur_service = UtilisateurService()
    with patch("src.webservice.dao.utilisateur_dao.UtilisateurDAO.supprimer_compte_DAO", side_effect=Exception("Database error")) as mock_supprimer:
        with pytest.raises(ValueError, match="Erreur lors de la suppression de l'utilisateur : Database error"):
            utilisateur_service.supprimer_compte(1)
        mock_supprimer.assert_called_once_with(1)

@patch('src.webservice.dao.utilisateur_dao.UtilisateurDAO.se_connecter_DAO')
def test_se_connecter_succes(mock_se_connecter, utilisateur_service):
    """
    Test de connexion réussie avec un mot de passe correct.
    """
    mot_de_passe_clair = "test_mdp"
    hashed_mdp, sel = hash_mdp(mot_de_passe_clair)
    mock_se_connecter.return_value = {
        "id_utilisateur": 1,
        "nom": "TestNom",
        "prenom": "TestPrenom",
        "pseudo": "TestPseudo",
        "adresse_mail": "test@test.com",
        "mdp": hashed_mdp,  # Mot de passe haché stocké dans la base
        "langue": "français",
        "sel": sel  # Le sel utilisé pour hacher le mot de passe
    }
    message = utilisateur_service.se_connecter(pseudo="TestPseudo", mdp=mot_de_passe_clair)
    assert message == "Bienvenue TestPseudo sur notre application"

@patch('src.webservice.dao.utilisateur_dao.UtilisateurDAO.se_connecter_DAO')
def test_se_connecter_echec(mock_se_connecter, utilisateur_service):

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

    mock_trouver_par_id.return_value = None

    with pytest.raises(ValueError, match="Utilisateur introuvable"):
        utilisateur_service.afficher(id_utilisateur=1)

@patch('src.webservice.dao.utilisateur_dao.UtilisateurDAO.existe_pseudo_DAO')
def test_verifier_pseudo(mock_existe_pseudo, utilisateur_service):
    """
    Test pour vérifier si le pseudo existe déjà dans la base de données.
    """
    pseudo_existe = "TestPseudoExist"
    mock_existe_pseudo.return_value = True  # Le pseudo existe déjà dans la base
    assert utilisateur_service.verifier_pseudo(pseudo_existe) is True
    pseudo_non_existe = "TestPseudoNonExist"
    mock_existe_pseudo.return_value = False
    assert utilisateur_service.verifier_pseudo(pseudo_non_existe) is False

@patch('src.webservice.dao.utilisateur_dao.UtilisateurDAO.existe_pseudo_DAO')
def test_verifier_pseudo_exception(mock_existe_pseudo, utilisateur_service):
    """
    Test pour vérifier le comportement en cas d'erreur dans la vérification du pseudo.
    """
    mock_existe_pseudo.side_effect = Exception("Problème de base de données")
    with pytest.raises(ValueError, match="Erreur lors de la vérification du pseudo : Problème de base de données"):
        utilisateur_service.verifier_pseudo("TestPseudo")