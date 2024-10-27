import unittest
from unittest.mock import MagicMock
from src.webservice.services.service_utilisateur import UtilisateurService
from src.webservice.business_object.utilisateur import Utilisateur

class TestUtilisateurService(unittest.TestCase):

    def setUp(self):
        # Créer un mock pour UtilisateurDAO
        self.mock_utilisateur_dao = MagicMock()

        # Créer une instance de UtilisateurService avec le DAO simulé
        self.utilisateur_service = UtilisateurService(utilisateur=self.mock_utilisateur_dao)

        # Définir un utilisateur pour les tests
        self.utilisateur = Utilisateur(
            id_utilisateur=123,
            nom="Alice",
            prenom="Dupont",
            pseudo="alice123",
            adresse_mail="alice@example.com",
            mdp="hashed_password",
            langue="français",
            sel="random_salt"
        )

    def test_creer_compte_succes(self):
        """
        Test de création de compte réussi
        """
        # Configurer le mock pour renvoyer un id_utilisateur (par exemple, 1)
        self.mock_utilisateur_dao.creer_compte_DAO.return_value = 1

        # Appeler la méthode à tester
        resultat = self.utilisateur_service.creer_compte(
            nom="Alice",
            prenom="Dupont",
            pseudo="alice123",
            adresse_mail="alice@example.com",
            mdp="password123",
            langue="français"
        )

        # Vérifier si le résultat est une instance de Utilisateur
        self.assertIsInstance(resultat, Utilisateur)
        self.assertEqual(resultat.nom, "Alice")
        self.assertEqual(resultat.pseudo, "alice123")


    def test_creer_compte_echec(self):
        """
        Test de création de compte échouée (pseudo déjà utilisé)
        """
        # Configurer le mock pour renvoyer False lors de la création de compte
        self.mock_utilisateur_dao.creer_compte_DAO.return_value = False

        # Appeler la méthode à tester
        resultat = self.utilisateur_service.creer_compte(
            nom="Alice",
            prenom="Dupont",
            pseudo="alice123",
            adresse_mail="alice@example.com",
            mdp="password123",
            langue="français"
        )

        # Vérifier si le résultat contient une erreur
        self.assertIsInstance(resultat, dict)
        self.assertIn("error", resultat)

    def test_se_connecter_succes(self):
        """
        Test de connexion réussie
        """
        # Configurer le mock pour renvoyer un utilisateur existant
        self.mock_utilisateur_dao.se_connecter_DAO.return_value = {
            "pseudo": "alice123",
            "mdp": self.utilisateur.mdp,
            "sel": self.utilisateur.sel
        }

        # Appeler la méthode à tester
        resultat = self.utilisateur_service.se_connecter(
            pseudo="alice123",
            mdp="password123"
        )

        # Vérifier si le message de bienvenue est correct
        self.assertEqual(resultat, f"Bienvenue alice123 sur notre application")
        self.mock_utilisateur_dao.se_connecter_DAO.assert_called_once_with("alice123")

    def test_se_connecter_echec(self):
        """
        Test de connexion échouée (pseudo non trouvé ou mauvais mot de passe)
        """
        # Configurer le mock pour renvoyer None (utilisateur non trouvé)
        self.mock_utilisateur_dao.se_connecter_DAO.return_value = None

        #  ValueError levée pour pseudo introuvable
        with self.assertRaises(ValueError) as context:
            self.utilisateur_service.se_connecter(
                pseudo="alice123",
                mdp="wrong_password"
            )

        self.assertEqual(str(context.exception), "Pseudo ou mot de passe incorrect.")
        self.mock_utilisateur_dao.se_connecter_DAO.assert_called_once_with("alice123")

        #  utilisateur existant mais mauvais mot de passe
        self.mock_utilisateur_dao.se_connecter_DAO.return_value = {
            "pseudo": "alice123",
            "mdp": "hashed_password_incorrect",
            "sel": "random_salt"
        }

        # Vérifier qu'une ValueError est levée pour mot de passe incorrect
        with self.assertRaises(ValueError) as context:
            self.utilisateur_service.se_connecter(
                pseudo="alice123",
                mdp="wrong_password"
            )

        self.assertEqual(str(context.exception), "Mot de passe incorrect.")
        self.mock_utilisateur_dao.se_connecter_DAO.assert_called_with("alice123")

    def test_supprimer_compte_succes(self):
        """
        Test de suppression de compte réussie
        """
        # Configurer le mock pour renvoyer l'utilisateur
        self.mock_utilisateur_dao.trouver_par_id.return_value = self.utilisateur
        self.mock_utilisateur_dao.supprimer_compte_DAO.return_value = True

        # Appeler la méthode à tester
        self.utilisateur_service.supprimer_compte(id_utilisateur="123")

        # Vérifier que la méthode de suppression a été appelée
        self.mock_utilisateur_dao.trouver_par_id.assert_called_once_with("123")
        self.mock_utilisateur_dao.supprimer_compte_DAO.assert_called_once_with(self.utilisateur)

    def test_supprimer_compte_utilisateur_inexistant(self):
        """
        Test de suppression de compte avec un utilisateur inexistant
        """
        # Configurer le mock pour renvoyer None (utilisateur non trouvé)
        self.mock_utilisateur_dao.trouver_par_id.return_value = None

        # Vérifier qu'une ValueError est levée
        with self.assertRaises(ValueError) as context:
            self.utilisateur_service.supprimer_compte(id_utilisateur="999")

        self.assertEqual(str(context.exception), "Utilisateur introuvable.")
        self.mock_utilisateur_dao.trouver_par_id.assert_called_once_with("999")

if __name__ == "__main__":
    unittest.main()
