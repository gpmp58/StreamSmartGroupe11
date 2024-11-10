from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.webservice.services.service_watchlist import WatchlistService
from src.webservice.dao.utilisateur_dao import UtilisateurDAO
from src.webservice.business_object.watchlist import Watchlist
from src.webservice.business_object.utilisateur import Utilisateur
from src.webservice.business_object.film import Film

# Création du router FastAPI
router = APIRouter()

# Initialisation des services et DAO
service_watchlist = WatchlistService()
utilisateur_dao = UtilisateurDAO()

# Modèle pour la création de Watchlist
class WatchlistCreateModel(BaseModel):
    nom_watchlist: str
    id_utilisateur: int

# Route pour créer une nouvelle watchlist
@router.post("/watchlists", response_model=dict)
async def creer_watchlist(watchlist_data: WatchlistCreateModel):
    """
    Crée une nouvelle watchlist pour un utilisateur.
    """
    try:
        # Étape 1 : Récupérer l'utilisateur par son ID
        utilisateur = utilisateur_dao.trouver_par_id(watchlist_data.id_utilisateur)
        if not utilisateur:
            raise HTTPException(status_code=404, detail="Utilisateur introuvable.")

        # Étape 2 : Créer la nouvelle watchlist
        nouvelle_watchlist = service_watchlist.creer_nouvelle_watchlist(
            nom_watchlist=watchlist_data.nom_watchlist,
            utilisateur=utilisateur
        )

        # Étape 3 : Vérifier le succès de la création et retourner la réponse
        if nouvelle_watchlist:
            return {
                "id_watchlist": nouvelle_watchlist.id_watchlist,
                "nom_watchlist": nouvelle_watchlist.nom_watchlist,
                "id_utilisateur": nouvelle_watchlist.id_utilisateur,
                "list_film": nouvelle_watchlist.get_list_film(),
            }
        else:
            raise HTTPException(status_code=400, detail="Erreur lors de la création de la watchlist.")

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Erreur interne : {e}")  # Affiche l'exception dans la console
        raise HTTPException(status_code=500, detail="Erreur interne du serveur.")


# Route pour supprimer une watchlist
@router.delete("/watchlists/{id_watchlist}")
async def supprimer_watchlist(id_watchlist: int):
    """
    Supprime une watchlist.
    """
    try:
        # Étape 1 : Créer un objet Watchlist avec seulement l'id_watchlist
        watchlist = Watchlist(nom_watchlist="", id_utilisateur=0, id_watchlist=id_watchlist)

        # Étape 2 : Supprimer la watchlist
        succes = service_watchlist.supprimer_watchlist(watchlist)

        # Étape 3 : Vérifier la suppression et retourner une réponse
        if succes:
            return {"message": f"La watchlist avec l'id '{id_watchlist}' a été supprimée avec succès."}
        else:
            raise HTTPException(status_code=400, detail="Erreur lors de la suppression de la watchlist.")

    except ValueError as e:
        print(f"Erreur connue : {e}")  # Affiche l'exception dans la console
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        print(f"Erreur interne : {e}")  # Affiche l'exception dans la console
        raise HTTPException(status_code=500, detail="Erreur interne du serveur.")


# Route pour ajouter un film à une watchlist
class AjouterFilmModel(BaseModel):
    id_watchlist: int
    id_film: int

@router.post("/watchlists/ajouter_film")
async def ajouter_film_watchlist(ajouter_film_data: AjouterFilmModel):
    """
    Ajoute un film à une watchlist.
    """
    try:
        # Étape 1 : Créer un objet Watchlist pour identifier la watchlist concernée
        watchlist = Watchlist(nom_watchlist="", id_utilisateur=0, id_watchlist=ajouter_film_data.id_watchlist)
        print(f"Watchlist créée : {watchlist.id_watchlist}")

        # Étape 2 : Créer un objet Film à partir de l'id_film
        film = Film(id_film=ajouter_film_data.id_film)
        print(f"Film à ajouter : {film.id_film}")

        # Étape 3 : Appeler le service pour ajouter le film à la watchlist
        succes_ajout = service_watchlist.ajouter_film(film=film, watchlist=watchlist)

        # Étape 4 : Vérifier le succès de l'ajout et retourner une réponse
        if succes_ajout:
            return {"message": f"Le film avec l'id '{ajouter_film_data.id_film}' a été ajouté à la watchlist."}
        else:
            raise HTTPException(status_code=400, detail="Erreur lors de l'ajout du film à la watchlist.")

    except ValueError as e:
        print(f"Erreur de valeur : {e}")  # Affichage supplémentaire pour identifier les problèmes
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(f"Erreur interne : {e}")  # Affichage pour déboguer l'exception non prévue
        raise HTTPException(status_code=500, detail="Erreur interne du serveur.")



# Route pour supprimer un film d'une watchlist
@router.delete("/watchlists/{id_watchlist}/supprimer_film/{id_film}")
async def supprimer_film_watchlist(id_watchlist: int, id_film: int):
    """
    Supprime un film d'une watchlist.
    """
    try:
        # Étape 1 : Créer un objet Watchlist pour identifier la watchlist concernée
        watchlist = Watchlist(nom_watchlist="", id_utilisateur=0, id_watchlist=id_watchlist)

        # Étape 2 : Créer un objet Film à partir de l'id_film
        film = Film(id_film=id_film)

        # Étape 3 : Appeler le service pour supprimer le film de la watchlist
        succes_suppression = service_watchlist.supprimer_film(film=film, watchlist=watchlist)

        # Étape 4 : Vérifier la suppression et retourner une réponse
        if succes_suppression:
            return {"message": f"Le film avec l'id '{id_film}' a été supprimé de la watchlist."}
        else:
            raise HTTPException(status_code=400, detail="Erreur lors de la suppression du film de la watchlist.")

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(f"Erreur interne : {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur.")


# Route pour récupérer tous les films d'une watchlist
@router.get("/watchlists/{id_watchlist}/films")
async def recuperer_films_watchlist(id_watchlist: int):
    """
    Récupère tous les films d'une watchlist.
    """
    try:
        # Étape 1 : Créer un objet Watchlist pour identifier la watchlist concernée
        watchlist = Watchlist(nom_watchlist="", id_utilisateur=0, id_watchlist=id_watchlist)

        # Étape 2 : Sauvegarder la watchlist et récupérer les films
        films = service_watchlist.sauvegarder_watchlist(watchlist)

        return {"films": films}

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(f"Erreur interne : {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur.")
