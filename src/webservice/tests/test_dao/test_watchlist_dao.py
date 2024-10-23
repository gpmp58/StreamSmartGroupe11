# Importation du module pystest pour créer les tests et de unittest.mock pour simuler les interactions avec la base de données
import pytest
from unittest.mock import patch, MagicMock

from src.webservice.dao.watchlist_dao import watchlistDao
from src.webservice.business_object.watchlist import watchlist
 
# Pour remplacer la connexion à la base de données par une version simulée.
@patch('src.webservice.dao.db_connection.DBConnection')
def test_creer_nouvelle_watchlist_DAO(MockDBConnection):
    # Given : Simuler une connexion à la base de données et un curseur
    mock_connection = MockDBConnection.return_value.connection
    mock_cursor = mock_connection.cursor.return_value.__enter__.return_value

    # Simuler un retour de requête
    mock_cursor.fetchone.return_value = {"id_watchlist": 1}
    
    # Créer une instance de watchlist
    wl = watchlist(nom_watchlist="My Watchlist", id_utilisateur=1)

    # When : Créer une instance de watchlistDao et appeler la méthode
    dao = watchlistDao()
    result = dao.creer_nouvelle_watchlist_DAO(wl)

    # Then : Vérifier que la méthode retourne True et que l'id_watchlist a été mis à jour
    assert result is True
    assert wl.id_watchlist == 1

    # Vérifier que les bonnes requêtes SQL ont été exécutées
    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO watchlist (nom_watchlist, id_utilisateur) "
        "VALUES (%(nom_watchlist)s, %(id_utilisateur)s) "
        "RETURNING id_watchlist;",
        {
            "nom_watchlist": "My Watchlist",
            "id_utilisateur": 1
        }
    )


@patch('src.webservice.dao.db_connection.DBConnection')
def test_supprimer_watchlist_DAO(MockDBConnection):
    # Given : Simuler une connexion à la base de données et un curseur
    mock_connection = MockDBConnection.return_value.connection
    mock_cursor = mock_connection.cursor.return_value.__enter__.return_value

    # Simuler une suppression réussie (rowcount = 1)
    mock_cursor.rowcount = 1

    # Créer une instance de watchlist
    wl = watchlist(id_watchlist=1)

    # When : Créer une instance de watchlistDao et appeler la méthode
    dao = watchlistDao()
    result = dao.supprimer_watchlist_DAO(wl)

    # Then : Vérifier que la méthode retourne True
    assert result is True

    # Vérifier que la bonne requête SQL a été exécutée
    mock_cursor.execute.assert_called_once_with(
        "DELETE FROM watchlist "
        " WHERE id_watchlist = %(id_watchlist)s",
        {"id_watchlist": 1}
    )


@patch('src.webservice.dao.db_connection.DBConnection')
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
        "INSERT INTO film_watchlist(id_watchlist, id_film) VALUES "
        "(%(id_watchlist)s, %(id_film)s);",
{"id_watchlist": 1, "id_film": 101}
    )


@patch('src.webservice.dao.db_connection.DBConnection')
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
        "DELETE FROM film_watchlist "
        "WHERE id_watchlist = %(id_watchlist)s and id_film = %(id_film)s",
        {"id_watchlist": 1, "id_film": 101}
    )
