from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.webservice.services.service_watchlist import WatchlistService
from src.webservice.business_object.watchlist import Watchlist
from src.webservice.business_object.film import Film

router = APIRouter()

# Initialisation du service watchlist
watchlist_service = WatchlistService()

# Modèle de données pour la création d'une watchlist
class WatchlistModel(BaseModel):
    nom_watchlist: str
    id_utilisateur: int

# Modèle de données pour la réponse de création de watchlist
class WatchlistDisplayModel(BaseModel):
    id_watchlist: int
    nom_watchlist: str
    id_utilisateur: int

# Modèle de données pour l'ajout d'un film dans la watchlist
class FilmModel(BaseModel):
    id_film: int

# 1. POST /watchlists : Créer une nouvelle watchlist
@router.post("/watchlists", response_model=WatchlistDisplayModel)
async def create_watchlist(watchlist: WatchlistModel):
    try:
        utilisateur_id = watchlist.id_utilisateur
        nouvelle_watchlist = watchlist_service.creer_nouvelle_watchlist(watchlist.nom_watchlist, utilisateur_id)
        if not nouvelle_watchlist:
            raise ValueError("Erreur lors de la création de la watchlist.")
        return WatchlistDisplayModel(
            id_watchlist=nouvelle_watchlist.id_watchlist,
            nom_watchlist=nouvelle_watchlist.nom_watchlist,
            id_utilisateur=nouvelle_watchlist.id_utilisateur,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# 2. DELETE /watchlists/{id_watchlist} : Supprimer une watchlist
@router.delete("/watchlists/{id_watchlist}")
async def delete_watchlist(id_watchlist: int):
    try:
        if not watchlist_service.supprimer_watchlist(id_watchlist):
            raise ValueError(f"Watchlist avec id '{id_watchlist}' non trouvée.")
        return {"message": f"Watchlist avec id '{id_watchlist}' supprimée avec succès."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# 3. POST /watchlists/{id_watchlist}/films : Ajouter un film à une watchlist
@router.post("/watchlists/{id_watchlist}/films")
async def add_film_to_watchlist(id_watchlist: int, film: FilmModel):
    try:
        film_obj = Film(film.id_film)  # Utilisation de la classe Film directement
        success = watchlist_service.ajouter_film(film_obj, id_watchlist)
        if not success:
            raise ValueError("Échec de l'ajout du film à la watchlist.")
        return {"message": f"Film avec id '{film.id_film}' ajouté à la watchlist avec id '{id_watchlist}'."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# 4. DELETE /watchlists/{id_watchlist}/films/{id_film} : Supprimer un film d'une watchlist
@router.delete("/watchlists/{id_watchlist}/films/{id_film}")
async def remove_film_from_watchlist(id_watchlist: int, id_film: int):
    try:
        film_obj = Film(id_film)  # Création d'une instance de Film directement
        success = watchlist_service.supprimer_film(film_obj, id_watchlist)
        if not success:
            raise ValueError("Film non trouvé dans la watchlist.")
        return {"message": f"Film avec id '{id_film}' supprimé de la watchlist avec id '{id_watchlist}'."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# 5. GET /watchlists/{id_watchlist}/films : Afficher les films d'une watchlist
@router.get("/watchlists/{id_watchlist}/films")
async def get_films_in_watchlist(id_watchlist: int):
    try:
        films = watchlist_service.sauvegarder_watchlist(id_watchlist)
        if not films:
            raise ValueError("Aucun film trouvé dans cette watchlist.")
        return {"films": films}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
