import unittest
from unittest.mock import MagicMock
from service.utilisateur_service import UtilisateurService
from business_object.utilisateur import Utilisateur

class TestUtilisateurService(unittest.TestCase):
    def setUp(self):
        # GIVEN: Une instance de UtilisateurDAO mockée et une instance de UtilisateurService
        self.mock_utilisateur_dao = MagicMock()
        self.service = UtilisateurService(utilisateur_dao=self.mock_utilisateur_dao)
        self.utilisateur = Utilisateur(
            nom="Alice",
            prenom="Dupont",
            pseudo="alice123",
            adresse_mail="alice@example.com",
            mdp="password123",
            langue="anglais"
        )

    def test_creer_compte_succes(self):
        # GIVEN: Un nouvel utilisateur avec des informations valides
        self.mock_utilisateur_dao.creer_compte_DAO.return_value = True

        # WHEN: On appelle la méthode creer_compte
        resultat = self.service.creer_compte(
            nom="Alice",
            prenom="Dupont",
            pseudo="alice123",
            adresse_mail="alice@example.com",
            mdp="password123",
            langue="anglais"
        )

        # THEN: Le compte est créé avec succès
        self.assertEqual(resultat, f"Nouveau compte créé : {self.utilisateur}")
        self.mock_utilisateur_dao.creer_compte_DAO.assert_called_once_with(self.utilisateur)

    def test_creer_compte_erreur_pseudo_existant(self):
        # GIVEN: Un pseudo déjà existant dans la base de données
        self.mock_utilisateur_dao.creer_compte_DAO.return_value = False

        # WHEN: On appelle la méthode creer_compte avec un pseudo déjà utilisé
        resultat = self.service.creer_compte(
            nom="Alice",
            prenom="Dupont",
            pseudo="alice123",
            adresse_mail="alice@example.com",
            mdp="password123",
            langue="anglais"
        )

        # THEN: Une erreur est renvoyée indiquant que le pseudo est déjà utilisé
        self.assertEqual(resultat, {"error": "Erreur lors de la création du compte. Le pseudo est peut-être déjà utilisé."})
        self.mock_utilisateur_dao.creer_compte_DAO.assert_called_once_with(self.utilisateur)

    def test_supprimer_compte_succes(self):
        # GIVEN: Un utilisateur existant dans la base de données
        self.mock_utilisateur_dao.trouver_par_pseudo.return_value = self.utilisateur

        # WHEN: On appelle la méthode supprimer_compte
        self.service.supprimer_compte(pseudo="alice123")

        # THEN: Le compte est supprimé avec succès
        self.mock_utilisateur_dao.supprimer_compte_DAO.assert_called_once_with(self.utilisateur)

    def test_supprimer_compte_utilisateur_inexistant(self):
        # GIVEN: Un pseudo qui n'existe pas dans la base de données
        self.mock_utilisateur_dao.trouver_par_pseudo.return_value = None

        # WHEN & THEN: On appelle la méthode supprimer_compte et une erreur est levée
        with self.assertRaises(ValueError) as context:
            self.service.supprimer_compte(pseudo="inconnu123")
        
        self.assertEqual(str(context.exception), "Utilisateur introuvable.")
        self.mock_utilisateur_dao.trouver_par_pseudo.assert_called_once_with("inconnu123")

    def test_se_connecter_succes(self):
        # GIVEN: Un utilisateur existant avec les bonnes informations de connexion
        self.mock_utilisateur_dao.se_connecter_DAO.return_value = self.utilisateur

        # WHEN: On appelle la méthode se_connecter avec les bons identifiants
        resultat = self.service.se_connecter(pseudo="alice123", mdp="password123")

        # THEN: Le message de bienvenue est renvoyé
        self.assertEqual(resultat, f"Bienvenue {self.utilisateur.pseudo} sur notre application")
        self.mock_utilisateur_dao.se_connecter_DAO.assert_called_once_with("alice123", "password123")

    def test_se_connecter_echec(self):
        # GIVEN: Un utilisateur avec un mauvais mot de passe
        self.mock_utilisateur_dao.se_connecter_DAO.return_value = None

        # WHEN & THEN: On appelle la méthode se_connecter et une erreur est levée
        with self.assertRaises(ValueError) as context:
            self.service.se_connecter(pseudo="alice123", mdp="wrongpassword")
        
        self.assertEqual(str(context.exception), "Pseudo ou mot de passe incorrect.")
        self.mock_utilisateur_dao.se_connecter_DAO.assert_called_once_with("alice123", "wrongpassword")

    def test_afficher_utilisateur_succes(self):
        # GIVEN: Un utilisateur existant dans la base de données
        self.mock_utilisateur_dao.trouver_par_pseudo.return_value = self.utilisateur

        # WHEN: On appelle la méthode afficher
        with self.assertLogs() as log:
            self.service.afficher(pseudo="alice123")

        # THEN: Les informations de l'utilisateur sont affichées
        self.assertIn(
            "Nom: Alice, Prénom: Dupont, Email: alice@example.com, Langue: anglais",
            log.output[0]
        )
        self.mock_utilisateur_dao.trouver_par_pseudo.assert_called_once_with("alice123")

    def test_afficher_utilisateur_inexistant(self):
        # GIVEN: Un pseudo qui n'existe pas dans la base de données
        self.mock_utilisateur_dao.trouver_par_pseudo.return_value = None

        # WHEN & THEN: On appelle la méthode afficher et une erreur est levée
        with self.assertRaises(ValueError) as context:
            self.service.afficher(pseudo="inconnu123")
        
        self.assertEqual(str(context.exception), "Utilisateur introuvable.")
        self.mock_utilisateur_dao.trouver_par_pseudo.assert_called_once_with("inconnu123")

if __name__ == "__main__":
    unittest.main()
