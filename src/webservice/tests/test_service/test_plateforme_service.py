import unittest
from unittest.mock import MagicMock, patch
from src.webservice.business_object.plateforme import PlateformeStreaming
from src.webservice.dao.plateforme_dao import PlateformeDAO
from src.webservice.dao.film_dao import FilmDao
from src.webservice.services.service_film import FilmService
from src.webservice.business_object.film import Film
from src.webservice.services.service_plateforme import ServicePlateforme

class TestServicePlateforme(unittest.TestCase):

    @patch.object(PlateformeDAO, 'verifier_plateforme_existe')
    @patch.object(PlateformeDAO, 'ajouter_plateforme')
    def test_mettre_a_jour_plateforme_plateforme_non_existante(self, mock_ajouter_plateforme, mock_verifier_plateforme_existe):
        # Test lorsque la plateforme n'existe pas encore
        mock_verifier_plateforme_existe.return_value = False
        mock_ajouter_plateforme.return_value = True
        
        service = ServicePlateforme()
        resultat = service.mettre_a_jour_plateforme("Netflix", 1)
        
        self.assertTrue(resultat)
        mock_verifier_plateforme_existe.assert_called_with(1, "Netflix")
        mock_ajouter_plateforme.assert_called_once()
    
    @patch.object(PlateformeDAO, 'verifier_plateforme_existe')
    def test_mettre_a_jour_plateforme_plateforme_existante(self, mock_verifier_plateforme_existe):
        # Test lorsque la plateforme existe déjà
        mock_verifier_plateforme_existe.return_value = True
        
        service = ServicePlateforme()
        resultat = service.mettre_a_jour_plateforme("Netflix", 1)
        
        self.assertFalse(resultat)
        mock_verifier_plateforme_existe.assert_called_with(1, "Netflix")

    @patch.object(PlateformeDAO, 'verifier_plateforme_existe')
    @patch.object(PlateformeDAO, 'ajouter_plateforme')
    def test_mettre_a_jour_plateforme_exception(self, mock_ajouter_plateforme, mock_verifier_plateforme_existe):
        # Test lorsqu'une exception est levée
        mock_verifier_plateforme_existe.side_effect = Exception("Erreur de base de données")
        
        service = ServicePlateforme()
        resultat = service.mettre_a_jour_plateforme("Netflix", 1)
        
        self.assertFalse(resultat)
        mock_verifier_plateforme_existe.assert_called_with(1, "Netflix")
    

    @patch.object(Film, 'recuperer_streaming')
    def test_ajouter_plateforme_sans_platforme(self, mock_recuperer_streaming):
        # Test lorsque le film ne retourne aucune plateforme
        film_mock = MagicMock(spec=Film)
        film_mock.id_film = 123
        mock_recuperer_streaming.return_value = []
        
        service = ServicePlateforme()
        service.mettre_a_jour_plateforme = MagicMock(return_value=True)
        
        service.ajouter_plateforme(film_mock)
        
        service.mettre_a_jour_plateforme.assert_not_called()

if __name__ == '__main__':
    unittest.main()
