from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from src.webservice.services.service_plateforme import ServicePlateforme
from src.webservice.business_object.film import Film

router = APIRouter()
service_plateforme = ServicePlateforme()


# Modèle pour ajouter une plateforme
class PlateformeModel(BaseModel):
    id_plateforme: int
    nom_plateforme: str


# Modèle pour ajouter des plateformes associées à un film
class FilmPlatformRequest(BaseModel):
    id_film: int
    streaming_info: List[PlateformeModel]


# Modèle de réponse
class PlateformeResponse(BaseModel):
    message: str


# 1. POST /api/plateformes/mettre-a-jour : Mettre à jour ou ajouter une plateforme
@router.post("/plateformes/mettre-a-jour", response_model=PlateformeResponse)
async def mettre_a_jour_plateforme(request: PlateformeModel):
    """
    Met à jour ou ajoute une nouvelle plateforme de streaming dans la base de données.

    - **id_plateforme**: ID unique de la plateforme.
    - **nom_plateforme**: Nom de la plateforme.
    """
    try:
        success = service_plateforme.mettre_a_jour_plateforme(
            nom_plateforme=request.nom_plateforme,
            id_plateforme=request.id_plateforme
        )
        if success:
            return {"message": f"La plateforme '{request.nom_plateforme}' a été ajoutée avec succès."}
        else:
            return {"message": f"La plateforme '{request.nom_plateforme}' existe déjà."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'opération : {str(e)}")


# 2. POST /api/plateformes/ajouter-par-film : Ajouter des plateformes associées à un film
@router.post("/plateformes/ajouter-par-film", response_model=PlateformeResponse)
async def ajouter_plateforme_par_film(request: FilmPlatformRequest):
    """
    Ajoute ou met à jour des plateformes associées à un film.

    - **id_film**: ID du film.
    - **streaming_info**: Liste des informations sur les plateformes associées au film.
    """
    try:
        # Conversion des données reçues en un objet `Film`
        film = Film(
            id_film=request.id_film,
            streaming_info=[{"id": p.id_plateforme, "name": p.nom_plateforme} for p in request.streaming_info]
        )
        service_plateforme.ajouter_plateforme(film)
        return {"message": "Les plateformes ont été ajoutées ou mises à jour avec succès pour le film."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'opération : {str(e)}")
