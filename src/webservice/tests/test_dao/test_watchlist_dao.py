# Importation du module pystest pour créer les tests et de unittest.mock pour simuler les interactions avec la base de données
import pytest
from unittest.mock import patch, MagicMock

from src.webservice.dao.watchlist_dao import watchlistDao
from src.webservice.business_object.watchlist import Watchlist

# Pour remplacer la connexion à la base de données par une version simulée.
@patch('dao.db_connection.DBConnection')
def test_creer_nouvelle_watchlist_DAO(MockDBConnection):
    # Given : Simuler une connexion à la base de données et un curseur
    mock_connection = MockDBConnection.return_value.connection
    mock_cursor = mock_connection.cursor.return_value.__enter__.return_value

    # Simuler un retour de requête
    mock_cursor.fetchone.return_value = {"id_watchlist": 1}
    
    # Créer une instance de Watchlist
    wl = Watchlist(nom_Watchlist="My Watchlist", id_utilisateur=1)

    # When : Créer une instance de watchlistDao et appeler la méthode
    dao = watchlistDao()
    result = dao.creer_nouvelle_Watchlist_DAO(wl)

    # Then : Vérifier que la méthode retourne True et que l'id_Watchlist a été mis à jour
    assert result is True
    assert wl.id_Watchlist == 1

    # Vérifier que les bonnes requêtes SQL ont été exécutées
    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO Watchlist (nom_Watchlist, id_utilisateur) "
        "VALUES (%(nom_Watchlist)s, %(id_utilisateur)s) "
        "RETURNING id_Watchlist;",
        {
            "nom_Watchlist": "My Watchlist",
            "id_utilisateur": 1
        }
    )


@patch('dao.db_connection.DBConnection')
def test_supprimer_Watchlist_DAO(MockDBConnection):
    # Given : Simuler une connexion à la base de données et un curseur
    mock_connection = MockDBConnection.return_value.connection
    mock_cursor = mock_connection.cursor.return_value.__enter__.return_value

    # Simuler une suppression réussie (rowcount = 1)
    mock_cursor.rowcount = 1

    # Créer une instance de Watchlist
    wl = Watchlist(id_Watchlist=1)

    # When : Créer une instance de watchlistDao et appeler la méthode
    dao = watchlistDao()
    result = dao.supprimer_Watchlist_DAO(wl)

    # Then : Vérifier que la méthode retourne True
    assert result is True

    # Vérifier que la bonne requête SQL a été exécutée
    mock_cursor.execute.assert_called_once_with(
        "DELETE FROM Watchlist "
        " WHERE id_Watchlist = %(id_Watchlist)s",
        {"id_Watchlist": 1}
    )


@patch('dao.db_connection.DBConnection')
def test_ajouter_film_DAO(MockDBConnection):
    # Given : Simuler une connexion à la base de données et un curseur
    mock_connection = MockDBConnection.return_value.connection
    mock_cursor = mock_connection.cursor.return_value.__enter__.return_value

    # Simuler une insertion réussie (rowcount = 1)
    mock_cursor.rowcount = 1

    # When : Créer une instance de watchlistDao et appeler la méthode
    dao = watchlistDao()
    result = dao.ajouter_film_DAO(1, 101)

    # Then : Vérifier que la méthode retourne True
    assert result is True

    # Vérifier que la bonne requête SQL a été exécutée
    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO film_Watchlist(id_Watchlist, id_film) VALUES "
        "(%(id_Watchlist)s, %(id_film)s);",
{"id_Watchlist": 1, "id_film": 101}
    )


@patch('dao.db_connection.DBConnection')
def test_supprimer_film_DAO(MockDBConnection):
    # Given : Simuler une connexion à la base de données et un curseur
    mock_connection = MockDBConnection.return_value.connection
    mock_cursor = mock_connection.cursor.return_value.__enter__.return_value

    # Simuler une suppression réussie (rowcount = 1)
    mock_cursor.rowcount = 1

    # When : Appeler la méthode supprimer_film_DAO
    dao = watchlistDao()
    result = dao.supprimer_film_DAO(1, 101)

    # Then : Vérifier que la méthode retourne True
    assert result is True

    # Vérifier que la bonne requête SQL a été exécutée
    mock_cursor.execute.assert_called_once_with(
        "DELETE FROM film_Watchlist "
        "WHERE id_Watchlist = %(id_Watchlist)s and id_film = %(id_film)s",
        {"id_Watchlist": 1, "id_film": 101}
    )
