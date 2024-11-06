from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict
from src.webservice.services.service_film import FilmService
from src.webservice.dao.film_dao import FilmDao


# Création du router FastAPI
router = APIRouter()

# Modèle de données pour rechercher un film
class RechercheFilmModel(BaseModel):
    nom_film: str

# 1. GET /films/recherche : Rechercher un film par nom
@router.post("/films/recherche")
async def rechercher_film(film: RechercheFilmModel):
    """
    Rechercher un film par son nom.
    
    Paramètres:
    ------------
    film : RechercheFilmModel
        Le nom du film que l'on souhaite rechercher.

    Returns:
    ---------
    dict : Liste des films trouvés avec leur id et titre original.
    """
    try:
        # Initialiser le service FilmService avec le nom du film
        film_service = FilmService(nom_film=film.nom_film)
        
        # Rechercher les films correspondant au nom donné
        films_trouves = film_service.rechercher_film()
        
        # Vérifier si une erreur est présente
        if 'error' in films_trouves:
            raise ValueError(films_trouves['error'])
        
        return {"films": films_trouves}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


