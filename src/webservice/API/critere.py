from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.webservice.services.service_critere import CritereService
from typing import Optional

router = APIRouter()


class CriteresModel(BaseModel):
    prix: Optional[bool] = None
    qualite: Optional[str] = None
    pub: Optional[bool] = None
    rapport_quantite_prix: Optional[bool] = None


class CritereRequestModel(BaseModel):
    id_watchlist: int
    criteres: CriteresModel


@router.post("/plateformes_film/")
async def recuperer_plateformes_film(critere: CritereRequestModel):
    critere_service = CritereService()
    try:
        plateformes = critere_service.recuperer_plateformes_film(
            critere
        )
        return plateformes
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=(
                "Erreur lors de la récupération des plateformes: "
                f"{str(e)}"
            ),
        )


@router.post("/filtrer_abonnement/")
async def filtrer_abonnement(critere: CritereRequestModel):
    critere_service = CritereService()
    critere.criteres = critere.criteres.dict()
    try:
        abonnements_filtrees = critere_service.filtrer_abonnement(
            critere
        )
        return abonnements_filtrees
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=(
                "Erreur lors du filtrage des abonnements: "
                f"{str(e)}"
            ),
        )


@router.post("/calculer_occurrences_plateformes/")
async def calculer_occurrences_plateformes(
    critere: CritereRequestModel,
):
    critere_service = CritereService()
    critere.criteres = critere.criteres.dict()
    try:
        occurrences = (
            critere_service.calculer_occurrences_plateformes(critere)
        )
        return occurrences
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=(
                "Erreur lors du calcul des occurrences de plateformes: "
                f"{str(e)}"
            ),
        )


@router.post("/optimiser_abonnement/")
async def optimiser_abonnement(critere: CritereRequestModel):
    critere_service = CritereService()
    critere.criteres = critere.criteres.dict()
    try:
        abonnement_optimise = critere_service.optimiser_abonnement(
            critere
        )
        if abonnement_optimise:
            return {
                "id_abonnement": abonnement_optimise.id_abonnement,
                "nom_plateforme": abonnement_optimise.nom_plateforme,
                "prix": abonnement_optimise.prix,
            }
        else:
            raise HTTPException(
                status_code=404,
                detail="Aucun abonnement optimisé trouvé.",
            )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=(
                "Erreur lors de l'optimisation de l'abonnement: "
                f"{str(e)}"
            ),
        )


@router.post("/afficher_abonnement_optimise/")
async def afficher_abonnement_optimise(critere: CritereRequestModel):
    critere_service = CritereService()
    critere.criteres = critere.criteres.dict()
    try:
        abonnement_resume = (
            critere_service.afficher_abonnement_optimise(critere)
        )
        return {"abonnement_optimise": abonnement_resume}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=(
                "Erreur lors de l'affichage de l'abonnement optimisé: "
                f"{str(e)}"
            ),
        )
