from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.webservice.business_object.film import Film
from src.webservice.services.service_plateforme import ServicePlateforme

router = APIRouter()
service_plateforme = ServicePlateforme()

class FilmModel(BaseModel):
    id_film: int

@router.post("/films/ajouter_plateformes", response_model=dict)
async def ajouter_plateformes(film_data: FilmModel):
    """
    Ajoute des plateformes de streaming pour un film donné.

    Attributs
    ----------
    FilmModel : Informations sur le film.
    """
    try:
        # Étape 1 : Construire l'objet Film
        film = Film(id_film=film_data.id_film)

        # Étape 2 : Utiliser le service pour ajouter les plateformes
        service_plateforme.ajouter_plateforme(film)

        return {"message": f"Les plateformes pour le film numéro : '{film_data.id_film}' ont été mises à jour avec succès."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne : {str(e)}")
