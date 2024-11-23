from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.webservice.business_object.film import Film
from src.webservice.services.service_plateforme import (
    ServicePlateforme,
)
import logging

# Configuration du logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)

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
    FilmModel : Informations sur le film. (juste l'id ici)
    """
    logger.info(
        f"Requête reçue pour ajouter "
        f"des plateformes au film ID: {film_data.id_film}"
    )

    try:
        # Étape 1 : Construire l'objet Film
        film = Film(id_film=film_data.id_film)
        print(film.recuperer_streaming())
        logger.debug(
            f"Film construit avec les détails : {film.details}"
        )

        # Étape 2 : Utiliser le service pour ajouter les plateformes
        logger.info(
            f"Ajout des plateformes pour le film ID: {film_data.id_film}"
        )
        service_plateforme.ajouter_plateforme(film)

        logger.info(
            f"Les plateformes pour le film ID: {film_data.id_film}"
            f" ont été mises à jour avec succès."
        )
        return {
            "message": f"Les plateformes pour le film "
            f"numéro : '{film_data.id_film}' ont été mises à jour avec succès."
        }

    except Exception as e:
        logger.error(
            f"Erreur lors de l'ajout des plateformes pour"
            f" le film ID: {film_data.id_film} : {str(e)}"
        )
        raise HTTPException(
            status_code=500, detail=f"Erreur interne : {str(e)}"
        )
