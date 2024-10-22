from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict
from src.webservice.services.service_film import FilmService
from src.webservice.dao.film_dao import FilmDao

# Création du router FastAPI
router = APIRouter()

# Initialisation du DAO et du service de film
film_dao = FilmDao()
film_service = None  # Nous allons l'initialiser lors de l'appel d'une route avec le nom du film.

# Modèle de données pour un film (utilisé pour l'API)
class FilmModel(BaseModel):
    id_film: int
    nom: str


# 1. GET /films/rechercher : Rechercher un film
@router.get("/films/rechercher", response_model=Dict[int, str])
async def rechercher_film(nom_film: str):
    """
    Rechercher un film par son nom.

    Paramètres:
    -----------
    nom_film : str
        Le nom du film à rechercher.

    Returns:
    --------
    Dict[int, str] : Une liste de films sous forme de dictionnaire, avec les id comme clés et les noms comme valeurs.
    """
    try:
        # Initialiser le FilmService avec le nom du film recherché
        film_service = FilmService(nom_film=nom_film)

        # Rechercher les films correspondants
        films_trouves = film_service.rechercher_film()

        # Vérifier s'il y a une erreur
        if "error" in films_trouves:
            raise HTTPException(status_code=400, detail=films_trouves["error"])

        return films_trouves

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur lors de la recherche du film.")

