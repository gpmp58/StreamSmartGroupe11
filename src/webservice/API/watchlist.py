from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from src.webservice.services.service_watchlist import WatchlistService
from src.webservice.business_object.watchlist import Watchlist
from src.webservice.business_object.film import Film
from src.webservice.dao.watchlist_dao import WatchlistDao

# Création du router FastAPI
router = APIRouter()

# Initialisation du service watchlist
watchlist_service = WatchlistService()

# Modèle de données pour une Watchlist (utilisé pour l'API)
class WatchlistModel(BaseModel):
    nom_watchlist: str
    id_utilisateur: int

class FilmModel(BaseModel):
    id_film: int
    nom: str

# 1. POST /watchlists : Créer une nouvelle watchlist
@router.post("/watchlists", response_model=WatchlistModel)
async def creer_watchlist(nom_watchlist: str, id_utilisateur: int):
    """
    Crée une nouvelle watchlist pour un utilisateur.

    Paramètres:
    -----------
    nom_watchlist : str
        Le nom de la nouvelle watchlist.
    id_utilisateur : int
        L'identifiant de l'utilisateur qui crée la watchlist.

    Returns:
    --------
    WatchlistModel : La watchlist créée avec succès.
    """
    try:
        # Création de la nouvelle watchlist via le service
        nouvelle_watchlist = watchlist_service.creer_nouvelle_watchlist(
            nom_watchlist=nom_watchlist,
            utilisateur=Watchlist(id_utilisateur=id_utilisateur)
        )
        if nouvelle_watchlist:
            return WatchlistModel(
                nom_watchlist=nouvelle_watchlist.nom_watchlist,
                id_utilisateur=nouvelle_watchlist.id_utilisateur
            )
        else:
            raise HTTPException(status_code=400, detail="Erreur lors de la création de la watchlist.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# 2. DELETE /watchlists/{id_watchlist} : Supprimer une watchlist
@router.delete("/watchlists/{id_watchlist}")
async def supprimer_watchlist(id_watchlist: int):
    """
    Supprime une watchlist existante.

    Paramètres:
    -----------
    id_watchlist : int
        L'identifiant de la watchlist à supprimer.

    Returns:
    --------
    dict : Message confirmant la suppression.
    """
    try:
        # Supprimer la watchlist en utilisant le service qui appelle le DAO
        watchlist = Watchlist(id_watchlist=id_watchlist)
        success = watchlist_service.supprimer_watchlist(watchlist)
        if success:
            return {"message": f"Watchlist '{id_watchlist}' supprimée avec succès"}
        else:
            raise HTTPException(status_code=400, detail="Erreur lors de la suppression de la watchlist.")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# 3. POST /watchlists/{id_watchlist}/films : Ajouter un film à une watchlist
@router.post("/watchlists/{id_watchlist}/films")
async def ajouter_film(id_watchlist: int, film: FilmModel):
    """
    Ajoute un film à une watchlist.

    Paramètres:
    -----------
    id_watchlist : int
        L'identifiant de la watchlist à laquelle ajouter le film.
    film : FilmModel
        Les informations du film à ajouter.

    Returns:
    --------
    dict : Message confirmant l'ajout.
    """
    try:
        # Ajouter un film à la watchlist via le service
        watchlist = Watchlist(id_watchlist=id_watchlist)
        film_obj = Film(id_film=film.id_film, nom=film.nom)
        success = watchlist_service.ajouter_film(film=film_obj, watchlist=watchlist)
        if success:
            return {"message": f"Film '{film.nom}' ajouté avec succès à la watchlist '{id_watchlist}'."}
        else:
            raise HTTPException(status_code=400, detail="Erreur lors de l'ajout du film à la watchlist.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# 4. DELETE /watchlists/{id_watchlist}/films/{id_film} : Supprimer un film d'une watchlist
@router.delete("/watchlists/{id_watchlist}/films/{id_film}")
async def supprimer_film(id_watchlist: int, id_film: int):
    """
    Supprime un film d'une watchlist.

    Paramètres:
    -----------
    id_watchlist : int
        L'identifiant de la watchlist.
    id_film : int
        L'identifiant du film à supprimer.

    Returns:
    --------
    dict : Message confirmant la suppression.
    """
    try:
        # Supprimer un film de la watchlist via le service
        watchlist = Watchlist(id_watchlist=id_watchlist)
        film_obj = Film(id_film=id_film, nom="")
        success = watchlist_service.supprimer_film(film=film_obj, watchlist=watchlist)
        if success:
            return {"message": f"Film '{id_film}' supprimé avec succès de la watchlist '{id_watchlist}'."}
        else:
            raise HTTPException(status_code=400, detail="Erreur lors de la suppression du film de la watchlist.")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# 5. GET /watchlists/{id_watchlist}/films : Récupérer les films d'une watchlist
@router.get("/watchlists/{id_watchlist}/films", response_model=List[FilmModel])
async def recuperer_films_watchlist(id_watchlist: int):
    """
    Récupère tous les films d'une watchlist spécifique.

    Paramètres:
    -----------
    id_watchlist : int
        L'identifiant de la watchlist.

    Returns:
    --------
    List[FilmModel] : Liste des films dans la watchlist.
    """
    try:
        # Sauvegarder la watchlist (récupérer les films de la watchlist) via le service
        watchlist = Watchlist(id_watchlist=id_watchlist)
        films = watchlist_service.sauvegarder_watchlist(watchlist)
        return [FilmModel(id_film=film.id_film, nom=film.nom) for film in films]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
