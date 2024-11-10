from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.webservice.services.service_watchlist import WatchlistService
from src.webservice.dao.utilisateur_dao import UtilisateurDAO
from src.webservice.business_object.watchlist import Watchlist

# Création du router FastAPI
router = APIRouter()

# Initialisation du service utilisateur et du service watchlist
utilisateur_dao = UtilisateurDAO()
watchlist_service = WatchlistService()

# Modèle pour la création de Watchlist
class WatchlistCreateModel(BaseModel):
    nom_watchlist: str
    id_utilisateur: int

# Route pour créer une nouvelle watchlist
@router.post("/watchlists")
async def creer_watchlist(watchlist_data: WatchlistCreateModel):
    """
    Crée une nouvelle watchlist pour un utilisateur.
    """
    try:
        # Récupérer l'utilisateur par son ID
        utilisateur = utilisateur_dao.trouver_par_id(watchlist_data.id_utilisateur)
        
        # Créer la nouvelle watchlist
        nouvelle_watchlist = watchlist_service.creer_nouvelle_watchlist(
            nom_watchlist=watchlist_data.nom_watchlist,
            utilisateur=utilisateur
        )

        if nouvelle_watchlist:
            return {
                "id_watchlist": nouvelle_watchlist.id_watchlist,
                "nom_watchlist": nouvelle_watchlist.nom_watchlist,
                "id_utilisateur": nouvelle_watchlist.id_utilisateur
            }
        else:
            raise HTTPException(status_code=400, detail="Erreur lors de la création de la watchlist.")

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# Route pour supprimer une watchlist
@router.delete("/watchlists/{id_watchlist}")
async def supprimer_watchlist(id_watchlist: int):
    """
    Supprime une watchlist.
    """
    try:
        # Étape 1 : Créer un objet Watchlist avec seulement l'id_watchlist
        watchlist = Watchlist(id_watchlist=id_watchlist, nom_watchlist="", id_utilisateur=0)
        
        # Étape 2 : Supprimer la watchlist
        succes = watchlist_service.supprimer_watchlist(watchlist)

        # Étape 3 : Vérifier la suppression et retourner une réponse
        if succes:
            return {"message": f"La watchlist avec l'id '{id_watchlist}' a été supprimée avec succès."}
        else:
            raise HTTPException(status_code=400, detail="Erreur lors de la suppression de la watchlist.")

    except ValueError as e:
        # Gérer les erreurs connues, comme l'absence de la watchlist dans la base
        print(f"Erreur connue : {e}")  # Affiche l'exception dans la console
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        # Gérer toute autre exception générale
        print(f"Erreur interne : {e}")  # Affiche l'exception dans la console
        raise HTTPException(status_code=500, detail="Erreur interne du serveur.")
