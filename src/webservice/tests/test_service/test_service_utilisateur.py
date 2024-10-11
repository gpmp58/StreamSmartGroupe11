import pytest
from unittest.mock import MagicMock
from src.webservice.services.service_utilisateur import UtilisateurService
from src.webservice.business_object.utilisateur import Utilisateur


# Fixture pour initialiser UtilisateurService et UtilisateurDAO
@pytest.fixture
def utilisateur_service():
    """
    Fixture pour initialiser le service UtilisateurService, le DAO simulé
    (MagicMock) et un objet Utilisateur de test.
    """
    mock_utilisateur_dao = MagicMock()
    service = UtilisateurService(utilisateur_dao=mock_utilisateur_dao)
    utilisateur = Utilisateur(
        nom="Alice",
        prenom="Dupont",
        pseudo="alice123",
        adresse_mail="alice@example.com",
        mdp="password123",
        langue="anglais"
    )
    return service, mock_utilisateur_dao, utilisateur


def test_creer_compte_succes(utilisateur_service):
    """
    Test de création de compte réussi : GIVEN un nouvel utilisateur, WHEN la
    méthode 'creer_compte' est appelée avec des informations valides, THEN
    le compte est créé avec succès.
    """
    service, mock_utilisateur_dao, utilisateur = utilisateur_service
    mock_utilisateur_dao.creer_compte_DAO.return_value = True

    # WHEN: On appelle la méthode creer_compte
    resultat = service.creer_compte(
        nom="Alice",
        prenom="Dupont",
        pseudo="alice123",
        adresse_mail="alice@example.com",
        mdp="password123",
        langue="anglais"
    )

    # THEN: Le compte est créé avec succès
    assert isinstance(resultat, Utilisateur)
    assert resultat.pseudo == "alice123"

    # Comparer les attributs
    mock_utilisateur_dao.creer_compte_DAO.assert_called_once()
    called_utilisateur = mock_utilisateur_dao.creer_compte_DAO.call_args[0][0]

    # Comparer les attributs des deux objets Utilisateur
    assert called_utilisateur.nom == utilisateur.nom
    assert called_utilisateur.prenom == utilisateur.prenom
    assert called_utilisateur.pseudo == utilisateur.pseudo
    assert called_utilisateur.adresse_mail == utilisateur.adresse_mail
    assert called_utilisateur.mdp == utilisateur.mdp
    assert called_utilisateur.langue == utilisateur.langue


def test_creer_compte_erreur_pseudo_existant(utilisateur_service):
    """
    Test de création de compte avec un pseudo existant : GIVEN un pseudo déjà
    existant, WHEN 'creer_compte' est appelée, THEN une erreur est levée.
    """
    service, mock_utilisateur_dao, utilisateur = utilisateur_service
    mock_utilisateur_dao.creer_compte_DAO.return_value = False

    # WHEN: On appelle la méthode creer_compte avec un pseudo déjà utilisé
    resultat = service.creer_compte(
        nom="Alice",
        prenom="Dupont",
        pseudo="alice123",
        adresse_mail="alice@example.com",
        mdp="password123",
        langue="anglais"
    )

    # THEN: Une erreur est renvoyée indiquant que le pseudo est déjà utilisé
    assert resultat == {"error": ("Erreur lors de la création du compte. "
                                  "Le pseudo est peut-être déjà utilisé.")}

    # Comparer les attributs du mock avec ceux de l'utilisateur attendu
    mock_utilisateur_dao.creer_compte_DAO.assert_called_once()
    called_utilisateur = mock_utilisateur_dao.creer_compte_DAO.call_args[0][0]

    assert called_utilisateur.nom == utilisateur.nom
    assert called_utilisateur.prenom == utilisateur.prenom
    assert called_utilisateur.pseudo == utilisateur.pseudo
    assert called_utilisateur.adresse_mail == utilisateur.adresse_mail
    assert called_utilisateur.mdp == utilisateur.mdp
    assert called_utilisateur.langue == utilisateur.langue


def test_supprimer_compte_succes(utilisateur_service):
    """
    Test de suppression de compte réussie : GIVEN un utilisateur existant,
    WHEN 'supprimer_compte' est appelée avec l'id de l'utilisateur, THEN le
    compte est supprimé avec succès.
    """
    service, mock_utilisateur_dao, utilisateur = utilisateur_service
    utilisateur.id_utilisateur = 1
    mock_utilisateur_dao.trouver_par_id.return_value = utilisateur

    # WHEN: On appelle la méthode supprimer_compte
    service.supprimer_compte(id_utilisateur=1)

    # THEN: Le compte est supprimé avec succès
    mock_utilisateur_dao.supprimer_compte_DAO.assert_called_once_with(
        utilisateur
    )


def test_supprimer_compte_utilisateur_inexistant(utilisateur_service):
    """
    Test de suppression de compte inexistant : GIVEN un id utilisateur qui
    n'existe pas, WHEN 'supprimer_compte' est appelée, THEN une erreur est
    levée.
    """
    service, mock_utilisateur_dao, _ = utilisateur_service
    mock_utilisateur_dao.trouver_par_id.return_value = None

    # WHEN & THEN: Appel de la méthode supprimer_compte et erreur est levée
    with pytest.raises(ValueError, match="Utilisateur introuvable."):
        service.supprimer_compte(id_utilisateur=999)


def test_se_connecter_succes(utilisateur_service):
    """
    Test de connexion réussie : GIVEN un utilisateur existant avec des bonnes
    informations de connexion, WHEN 'se_connecter' est appelée, THEN un
    message de bienvenue est retourné.
    """
    service, mock_utilisateur_dao, utilisateur = utilisateur_service
    mock_utilisateur_dao.se_connecter_DAO.return_value = utilisateur

    # WHEN: On appelle la méthode se_connecter avec les bons identifiants
    resultat = service.se_connecter(pseudo="alice123", mdp="password123")

    # THEN: Le message de bienvenue est renvoyé
    assert resultat == f"Bienvenue {utilisateur.pseudo} sur notre application"
    mock_utilisateur_dao.se_connecter_DAO.assert_called_once_with(
        "alice123", "password123"
    )


def test_se_connecter_echec(utilisateur_service):
    """
    Test de connexion échouée : GIVEN un utilisateur avec un mauvais mot de
    passe, WHEN 'se_connecter' est appelée, THEN une erreur est levée.
    """
    service, mock_utilisateur_dao, _ = utilisateur_service
    mock_utilisateur_dao.se_connecter_DAO.return_value = None

    # WHEN & THEN: On appelle la méthode se_connecter et une erreur est levée
    with pytest.raises(ValueError, match="Pseudo ou mot de passe incorrect."):
        service.se_connecter(pseudo="alice123", mdp="wrongpassword")


def test_afficher_utilisateur_succes(utilisateur_service, capsys):
    """
    Test d'affichage des informations d'un utilisateur réussi : GIVEN un
    utilisateur existant, WHEN 'afficher' est appelée, THEN les informations
    de l'utilisateur sont affichées correctement.
    """
    service, mock_utilisateur_dao, utilisateur = utilisateur_service
    utilisateur.id_utilisateur = 1
    mock_utilisateur_dao.trouver_par_id.return_value = utilisateur

    # WHEN: On appelle la méthode afficher
    service.afficher(id_utilisateur=1)

    # THEN: Les informations de l'utilisateur sont affichées
    captured = capsys.readouterr()
    assert ("Nom: Alice, Prénom: Dupont, Email: alice@example.com, Langue: "
            "anglais" in captured.out)
    mock_utilisateur_dao.trouver_par_id.assert_called_once_with(1)


def test_afficher_utilisateur_inexistant(utilisateur_service):
    """
    Test d'affichage d'un utilisateur inexistant : GIVEN un id utilisateur
    qui n'existe pas, WHEN 'afficher' est appelée, THEN une erreur est levée.
    """
    service, mock_utilisateur_dao, _ = utilisateur_service
    mock_utilisateur_dao.trouver_par_id.return_value = None

    # WHEN & THEN: On appelle la méthode afficher et une erreur est levée
    with pytest.raises(ValueError, match="Utilisateur introuvable."):
        service.afficher(id_utilisateur=999)
