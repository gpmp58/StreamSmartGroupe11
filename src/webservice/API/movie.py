from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from src.webservice.services.service_film import FilmService
from src.webservice.business_object.film import Film

router = APIRouter()

# Modèle de données pour rechercher un film
class RechercheFilmModel(BaseModel):
    nom_film: str

# Modèle de réponse pour les films trouvés
class FilmTrouve(BaseModel):
    id: int
    titre_original: str
    date_sortie: str
    vote_average: float

class RechercheFilmResponse(BaseModel):
    films: List[FilmTrouve]

# Modèle pour les services de streaming
class StreamingProvider(BaseModel):
    id: int
    name: str
    logo: str

# Modèle de réponse pour les détails du film
class FilmDetails(BaseModel):
    name: str
    description: str
    sortie: str
    vote_average: float
    date_sortie: str
    duree: str
    genres: List[str]
    image: str
    streaming: List[StreamingProvider]

# 1. POST /api/films/recherche : Rechercher un film par nom
@router.post("/films/recherche", response_model=RechercheFilmResponse)
async def rechercher_film(film: RechercheFilmModel):
    """
    Rechercher un film par son nom.

    - **nom_film**: Nom du film à rechercher.
    """
    try:
        # Initialiser le service FilmService avec le nom du film
        film_service = FilmService(nom_film=film.nom_film)
        
        # Rechercher les films correspondant au nom donné
        films_trouves = film_service.rechercher_film()
        
        # Vérifier si une erreur est présente
        if isinstance(films_trouves, dict) and 'error' in films_trouves:
            raise ValueError(films_trouves['error'])
        
        return {"films": films_trouves}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

# 2. GET /api/films/{id_film} : Obtenir les détails d'un film par ID
@router.get("/films/{id_film}", response_model=FilmDetails)
async def get_film_details(id_film: int):
    """
    Récupère les détails d'un film en fonction de son ID TMDb.

    - **id_film**: ID du film dans TMDb
    """
    try:
        film = Film(id_film)
        print("Détails du film:", film.details)  # Pour débogage
        response = {
            "name": film.details["name"],
            "description": film.details["description"],
            "sortie": film.details["sortie"],
            "vote_average": float(film.details["vote_average"]),  
            "date_sortie": film.details["date_sortie"],
            "duree": film.details["duree"],
            "genres": film.details["genres"],
            "image": film.image,
            "streaming": film.streaming  
        }
        return response
    except KeyError as e:
        raise HTTPException(status_code=500, detail=f"Clé manquante dans les détails du film : {e}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Erreur de validation des données : {e}")
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
