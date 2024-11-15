# src/webservice/API/watchlist.py

import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.webservice.services.service_watchlist import WatchlistService
from src.webservice.dao.utilisateur_dao import UtilisateurDAO
from src.webservice.business_object.watchlist import Watchlist
from src.webservice.business_object.utilisateur import Utilisateur
from src.webservice.business_object.film import Film
from src.webservice.dao.film_dao import FilmDao


router = APIRouter()

# Initialisation des services et DAO
service_watchlist = WatchlistService()
utilisateur_dao = UtilisateurDAO()

# Configuration du logger
logger = logging.getLogger(__name__)

# Modèle pour la création de Watchlist
class WatchlistCreateModel(BaseModel):
    nom_watchlist: str
    id_utilisateur: int

# Route pour créer une nouvelle watchlist
@router.post("/watchlists", response_model=dict)
async def creer_watchlist(watchlist_data: WatchlistCreateModel):
    """
    Crée une nouvelle watchlist pour un utilisateur.
    """
    try:
        # Étape 1 : Récupérer l'utilisateur par son ID
        utilisateur = utilisateur_dao.trouver_par_id(watchlist_data.id_utilisateur)
        if not utilisateur:
            logger.warning(f"Utilisateur avec id {watchlist_data.id_utilisateur} introuvable.")
            raise HTTPException(status_code=404, detail="Utilisateur introuvable.")

        # Étape 2 : Créer la nouvelle watchlist
        nouvelle_watchlist = service_watchlist.creer_nouvelle_watchlist(
            nom_watchlist=watchlist_data.nom_watchlist,
            utilisateur=utilisateur
        )

        # Étape 3 : Vérifier le succès de la création et retourner la réponse
        if nouvelle_watchlist:
            logger.info(f"Watchlist créée avec id {nouvelle_watchlist.id_watchlist}.")
            return {
                "id_watchlist": nouvelle_watchlist.id_watchlist,
                "nom_watchlist": nouvelle_watchlist.nom_watchlist,
                "id_utilisateur": nouvelle_watchlist.id_utilisateur,
                "list_film": nouvelle_watchlist.get_list_film(),
            }
        else:
            logger.error("Erreur lors de la création de la watchlist.")
            raise HTTPException(status_code=400, detail="Erreur lors de la création de la watchlist.")

    except ValueError as e:
        logger.error(f"Erreur de valeur : {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(f"Erreur interne lors de la création de la watchlist : {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur.")

# Route pour supprimer une watchlist
@router.delete("/watchlists/{id_watchlist}")
async def supprimer_watchlist(id_watchlist: int):
    """
    Supprime une watchlist.
    """
    try:
        # Étape 1 : Créer un objet Watchlist avec seulement l'id_watchlist
        watchlist = Watchlist(nom_watchlist="", id_utilisateur=0, id_watchlist=id_watchlist)

        # Étape 2 : Supprimer la watchlist
        succes = service_watchlist.supprimer_watchlist(watchlist)

        # Étape 3 : Vérifier la suppression et retourner une réponse
        if succes:
            logger.info(f"Watchlist avec id {id_watchlist} supprimée avec succès.")
            return {"message": f"La watchlist avec l'id '{id_watchlist}' a été supprimée avec succès."}
        else:
            logger.error(f"Erreur lors de la suppression de la watchlist avec id {id_watchlist}.")
            raise HTTPException(status_code=400, detail="Erreur lors de la suppression de la watchlist.")

    except ValueError as e:
        logger.error(f"Erreur connue lors de la suppression : {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception(f"Erreur interne lors de la suppression de la watchlist : {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur.")

class AjouterFilmModel(BaseModel):
    id_watchlist: int
    id_film: int
    #nom_film: str  # Nom du film pour l'ajout à la table 'film'

@router.post("/watchlists/ajouter_film", response_model=dict)
async def ajouter_film_watchlist(ajouter_film_data: AjouterFilmModel):
    """
    Ajoute un film à une watchlist.
    #Il faut d'abord sauvegarder PUIS ajouter
    
    """
    try:
        # Étape 1 : Créer un objet Watchlist pour identifier la watchlist concernée
        watchlist = Watchlist(
            nom_watchlist="",  # Vous pouvez récupérer le nom de la watchlist depuis la base de données si nécessaire
            id_utilisateur=0,  # Assurez-vous d'obtenir l'id_utilisateur approprié
            id_watchlist=ajouter_film_data.id_watchlist
        )
        logger.debug(f"Watchlist créée : {watchlist.id_watchlist}")

        # Étape 2 : Créer un objet Film à partir de l'id_film et du nom_film
        film = Film(
            id_film=ajouter_film_data.id_film
        )
        nom_film=film.details["name"]
        logger.debug(f"Film à ajouter : {film.id_film} ")
        # Étape 4 : Appeler le service pour ajouter le film à la watchlist
        succes_ajout = service_watchlist.ajouter_film(film=film, watchlist=watchlist)

        # Étape 5 : Vérifier le succès de l'ajout et retourner une réponse
        if succes_ajout:
            logger.info(f"Le film avec l'id '{ajouter_film_data.id_film}' a été ajouté à la watchlist {ajouter_film_data.id_watchlist}.")
            return {"message": f"Le film avec l'id '{ajouter_film_data.id_film}' a été ajouté à la watchlist."}
        else:
            logger.warning(f"Le film avec l'id '{ajouter_film_data.id_film}' est déjà présent dans la watchlist {ajouter_film_data.id_watchlist}.")
            raise HTTPException(status_code=400, detail="Erreur lors de l'ajout du film à la watchlist.")

    except ValueError as e:
        logger.error(f"Erreur de valeur lors de l'ajout du film : {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception(f"Erreur interne lors de l'ajout du film à la watchlist : {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur.")

# Route pour supprimer un film d'une watchlist
@router.delete("/watchlists/{id_watchlist}/supprimer_film/{id_film}")
async def supprimer_film_watchlist(id_watchlist: int, id_film: int):
    """
    Supprime un film d'une watchlist.
    """
    try:
        # Étape 1 : Créer un objet Watchlist pour identifier la watchlist concernée
        watchlist = Watchlist(nom_watchlist="", id_utilisateur=0, id_watchlist=id_watchlist)

        # Étape 2 : Créer un objet Film à partir de l'id_film
        film = Film(id_film=id_film)

        # Étape 3 : Appeler le service pour supprimer le film de la watchlist
        succes_suppression = service_watchlist.supprimer_film(Film=film, watchlist=watchlist)

        # Étape 4 : Vérifier la suppression et retourner une réponse
        if succes_suppression:
            logger.info(f"Le film avec l'id '{id_film}' a été supprimé de la watchlist {id_watchlist}.")
            return {"message": f"Le film avec l'id '{id_film}' a été supprimé de la watchlist."}
        else:
            logger.error(f"Erreur lors de la suppression du film avec id {id_film} de la watchlist {id_watchlist}.")
            raise HTTPException(status_code=400, detail="Erreur lors de la suppression du film de la watchlist.")

    except ValueError as e:
        logger.error(f"Erreur de valeur lors de la suppression du film : {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception(f"Erreur interne lors de la suppression du film de la watchlist : {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur.")

# Route pour récupérer tous les films d'une watchlist
@router.get("/watchlists/{id_watchlist}/films", response_model=dict)
async def recuperer_films_watchlist(id_watchlist: int):
    """
    Récupère tous les films d'une watchlist.
    """
    try:
        # Étape 1 : Créer un objet Watchlist pour identifier la watchlist concernée
        watchlist = Watchlist(nom_watchlist="", id_utilisateur=0, id_watchlist=id_watchlist)

        # Étape 2 : Sauvegarder la watchlist et récupérer les films
        films = service_watchlist.sauvegarder_watchlist(watchlist)

        logger.info(f"Récupération des films pour la watchlist {id_watchlist} réussie.")
        return {"films": films}

    except ValueError as e:
        logger.error(f"Erreur de valeur lors de la récupération des films : {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception(f"Erreur interne lors de la récupération des films de la watchlist : {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur.")

@router.get("/watchlists/utilisateur/{id_utilisateur}", response_model=dict)
async def afficher_watchlist(id_utilisateur: int):
    """
    Récupère toutes les watchlists d'un utilisateur spécifique, avec les films associés.
    """
    try:
        # Étape 1 : Récupérer l'utilisateur par son ID
        utilisateur = utilisateur_dao.trouver_par_id(id_utilisateur)
        if not utilisateur:
            logger.warning(f"Utilisateur avec id {id_utilisateur} introuvable.")
            raise HTTPException(status_code=404, detail="Utilisateur introuvable.")

        # Étape 2 : Utiliser le service pour récupérer les watchlists de l'utilisateur
        watchlists = service_watchlist.afficher_watchlist(id_utilisateur)

        # Étape 3 : Retourner les watchlists et leurs films associés
        logger.info(f"Watchlists récupérées pour l'utilisateur {id_utilisateur}.")
        return {"watchlists": watchlists}

    except ValueError as e:
        logger.error(f"Erreur de valeur lors de la récupération des watchlists : {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(f"Erreur interne lors de la récupération des watchlists : {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur.")
