import unittest
from unittest.mock import MagicMock
from src.webservice.services.service_watchlist import WatchlistService
from src.webservice.business_object.watchlist import Watchlist
from src.webservice.dao.watchlist_dao import WatchlistDao


class ClassWatchlistTest(unittest.TestCase):

    def test_creer_nouvelle_watchlist_ok(self):
        """Création de nouvelle watchlist réussie"""

        nom_watchlist = "Ma Nouvelle Watchlist"
        id_utilisateur = 1 
        utilisateur = MagicMock()
        utilisateur.id_utilisateur = id_utilisateur
        WatchlistDao.creer_nouvelle_watchlist_DAO = MagicMock(return_value=True)
        watchlist = WatchlistService().creer_nouvelle_watchlist(nom_watchlist, utilisateur)
        assert watchlist.nom_watchlist == "Ma Nouvelle Watchlist"
        assert watchlist.id_utilisateur == id_utilisateur

    def test_creer_nouvelle_watchlist_fail(self):
        nom_watchlist = "Ma Nouvelle Watchlist"
        id_utilisateur = 1 
        utilisateur = MagicMock()
        utilisateur.id_utilisateur = id_utilisateur
        WatchlistDao.creer_nouvelle_watchlist_DAO = MagicMock(return_value=False)
        watchlist = WatchlistService().creer_nouvelle_watchlist(nom_watchlist, utilisateur)
        assert watchlist is None

    
    def test_ajouter_film_ok(self):
        """Ajout d'un film à la watchlist réussie"""
        # GIVEN
        id_film = 1
        id_watchlist = 1
        nom_film = "Film Test"

        film = MagicMock()
        film.id_film = id_film
        film.nom_film = nom_film

        watchlist = MagicMock()
        watchlist.id_watchlist = id_watchlist

        WatchlistDao().film_deja_present = MagicMock(return_value=False)
        WatchlistDao().ajouter_film_DAO = MagicMock(return_value=True)

        # WHEN
        result = WatchlistService().ajouter_film(film, watchlist)

        # THEN
        assert result is True
        WatchlistDao().film_deja_present.assert_called_once_with(id_watchlist, id_film)
        WatchlistDao().ajouter_film_DAO.assert_called_once_with(id_watchlist, id_film)
    
    def test_ajouter_film_deja_present(self):
        """Le film est déjà présent dans la watchlist"""

        # GIVEN
        id_film = 1
        id_watchlist = 1

        film = MagicMock()
        film.id_film = id_film

        watchlist = MagicMock()
        watchlist.id_watchlist = id_watchlist

        WatchlistDao().film_deja_present = MagicMock(return_value=True)

        # WHEN
        result = WatchlistService().ajouter_film(film, watchlist)

        # THEN
        assert result is False
        WatchlistDao().film_deja_present.assert_called_once_with(id_watchlist, id_film)
        WatchlistDao().ajouter_film_DAO.assert_not_called()
