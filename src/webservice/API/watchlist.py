from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.webservice.services.service_watchlist import WatchlistService
from src.webservice.dao.utilisateur_dao import UtilisateurDAO
from src.webservice.business_object.watchlist import Watchlist
from src.webservice.business_object.utilisateur import Utilisateur
from src.webservice.business_object.film import Film
from src.webservice.services.service_plateforme import ServicePlateforme

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
<<<<<<< HEAD
        utilisateur = utilisateur_dao.trouver_par_id(watchlist_data.id_utilisateur)
        if not utilisateur:
=======
        # Étape 1 : Récupérer l'utilisateur par son ID
        utilisateur = utilisateur_dao.trouver_par_id(watchlist_data.id_utilisateur)
        if not utilisateur:
            logger.warning(
                f"Utilisateur avec id {watchlist_data.id_utilisateur} introuvable."
            )
>>>>>>> a73b05db2e8e2645eb8c912745b3cb85574b99eb
            raise HTTPException(status_code=404, detail="Utilisateur introuvable.")

        nouvelle_watchlist = service_watchlist.creer_nouvelle_watchlist(
            nom_watchlist=watchlist_data.nom_watchlist,
            utilisateur=utilisateur
        )

        if nouvelle_watchlist:
<<<<<<< HEAD
=======
            logger.info(f"Watchlist créée avec id {nouvelle_watchlist.id_watchlist}.")
>>>>>>> a73b05db2e8e2645eb8c912745b3cb85574b99eb
            return {
                "id_watchlist": nouvelle_watchlist.id_watchlist,
                "nom_watchlist": nouvelle_watchlist.nom_watchlist,
                "id_utilisateur": nouvelle_watchlist.id_utilisateur,
                "list_film": nouvelle_watchlist.get_list_film(),
            }
        else:
<<<<<<< HEAD
            raise HTTPException(status_code=400, detail="Erreur lors de la création de la watchlist.")
=======
            logger.error("Erreur lors de la création de la watchlist.")
            raise HTTPException(
                status_code=400, detail="Erreur lors de la création de la watchlist."
            )
>>>>>>> a73b05db2e8e2645eb8c912745b3cb85574b99eb

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
<<<<<<< HEAD
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur interne du serveur.")
=======
    except Exception as e:
        logger.exception(f"Erreur interne lors de la création de la watchlist : {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur.")

>>>>>>> a73b05db2e8e2645eb8c912745b3cb85574b99eb

# Route pour supprimer une watchlist
@router.delete("/watchlists/{id_watchlist}")
async def supprimer_watchlist(id_watchlist: int):
    """
    Supprime une watchlist.
    """
    try:
        watchlist = Watchlist(nom_watchlist="", id_utilisateur=0, id_watchlist=id_watchlist)
        succes = service_watchlist.supprimer_watchlist(watchlist)

        if succes:
<<<<<<< HEAD
            return {"message": f"La watchlist avec l'id '{id_watchlist}' a été supprimée avec succès."}
        else:
            raise HTTPException(status_code=400, detail="Erreur lors de la suppression de la watchlist.")
=======
            logger.info(f"Watchlist avec id {id_watchlist} supprimée avec succès.")
            return {
                "message": f"La watchlist avec l'id '{id_watchlist}' a été supprimée avec succès."
            }
        else:
            logger.error(
                f"Erreur lors de la suppression de la watchlist avec id {id_watchlist}."
            )
            raise HTTPException(
                status_code=400, detail="Erreur lors de la suppression de la watchlist."
            )
>>>>>>> a73b05db2e8e2645eb8c912745b3cb85574b99eb

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
<<<<<<< HEAD
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur interne du serveur.")
=======
    except Exception as e:
        logger.exception(f"Erreur interne lors de la suppression de la watchlist : {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur.")

>>>>>>> a73b05db2e8e2645eb8c912745b3cb85574b99eb

class AjouterFilmModel(BaseModel):
    id_watchlist: int
    id_film: int

@router.post("/watchlists/ajouter_film", response_model=dict)
async def ajouter_film_watchlist(ajouter_film_data: AjouterFilmModel):
    """
    Ajoute un film à une watchlist, puis associe le film à ses plateformes.
    """
    try:
        watchlist = Watchlist(nom_watchlist="", id_utilisateur=0, id_watchlist=ajouter_film_data.id_watchlist)
        film = Film(id_film=ajouter_film_data.id_film)
<<<<<<< HEAD
=======
        nom_film = film.details["name"]
        logger.debug(f"Film à ajouter : {film.id_film}")

        # Étape 3 : Ajouter le film à la watchlist
        succes_ajout = service_watchlist.ajouter_film(film=film, watchlist=watchlist)
>>>>>>> a73b05db2e8e2645eb8c912745b3cb85574b99eb

        succes_ajout = service_watchlist.ajouter_film(film=film, watchlist=watchlist)
        if not succes_ajout:
<<<<<<< HEAD
            raise HTTPException(status_code=400, detail="Erreur lors de l'ajout du film à la watchlist.")
=======
            logger.warning(
                f"Le film avec l'id '{ajouter_film_data.id_film}' ne peut pas être ajouté dans la watchlist {ajouter_film_data.id_watchlist}."
            )
            raise HTTPException(
                status_code=400, detail="Erreur lors de l'ajout du film à la watchlist."
            )
>>>>>>> a73b05db2e8e2645eb8c912745b3cb85574b99eb

        streaming_info = film.recuperer_streaming()
        for plateforme in streaming_info:
            id_plateforme = plateforme.get("id")
            nom_plateforme = plateforme.get("name")

            if id_plateforme and nom_plateforme:
                ServicePlateforme().mettre_a_jour_plateforme(nom_plateforme, id_plateforme)
                ServicePlateforme().ajouter_plateforme(film)

<<<<<<< HEAD
        return {"message": f"Le film avec l'id '{ajouter_film_data.id_film}' a été ajouté à la watchlist et associé à ses plateformes."}
=======
            success_plateforme = ServicePlateforme().mettre_a_jour_plateforme(
                nom_plateforme, id_plateforme
            )
            if success_plateforme:
                logger.info(f"Plateforme '{nom_plateforme}' ajoutée avec succès.")
            else:
                logger.info(f"Plateforme '{nom_plateforme}' existe déjà.")
            # Etape 5 : Mise a jour table plateforme_film
            ServicePlateforme().ajouter_plateforme(film)

        logger.info(
            f"Le film avec l'id '{ajouter_film_data.id_film}' a été ajouté à la watchlist {ajouter_film_data.id_watchlist} et associé à ses plateformes."
        )
        return {
            "message": f"Le film avec l'id '{ajouter_film_data.id_film}' a été ajouté à la watchlist et associé à ses plateformes."
        }
>>>>>>> a73b05db2e8e2645eb8c912745b3cb85574b99eb

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
<<<<<<< HEAD
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur interne du serveur.")
=======
    except Exception as e:
        logger.exception(f"Erreur interne lors de l'ajout du film à la watchlist : {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur.")

>>>>>>> a73b05db2e8e2645eb8c912745b3cb85574b99eb

# Route pour supprimer un film d'une watchlist
@router.delete("/watchlists/{id_watchlist}/supprimer_film/{id_film}")
async def supprimer_film_watchlist(id_watchlist: int, id_film: int):
    """
    Supprime un film d'une watchlist.
    """
    try:
        watchlist = Watchlist(nom_watchlist="", id_utilisateur=0, id_watchlist=id_watchlist)
        film = Film(id_film=id_film)

        succes_suppression = service_watchlist.supprimer_film(Film=film, watchlist=watchlist)

        if succes_suppression:
<<<<<<< HEAD
            return {"message": f"Le film avec l'id '{id_film}' a été supprimé de la watchlist."}
=======
            logger.info(
                f"Le film avec l'id '{id_film}' a été supprimé de la watchlist {id_watchlist}."
            )
            return {
                "message": f"Le film avec l'id '{id_film}' a été supprimé de la watchlist."
            }
>>>>>>> a73b05db2e8e2645eb8c912745b3cb85574b99eb
        else:
            raise HTTPException(status_code=400, detail="Erreur lors de la suppression du film de la watchlist.")

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
<<<<<<< HEAD
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur interne du serveur.")
=======
    except Exception as e:
        logger.exception(
            f"Erreur interne lors de la suppression du film de la watchlist : {e}"
        )
        raise HTTPException(status_code=500, detail="Erreur interne du serveur.")

>>>>>>> a73b05db2e8e2645eb8c912745b3cb85574b99eb

# Route pour récupérer tous les films d'une watchlist
@router.get("/watchlists/{id_watchlist}/films", response_model=dict)
async def recuperer_films_watchlist(id_watchlist: int):
    """
    Récupère tous les films d'une watchlist.
    """
    try:
        watchlist = Watchlist(nom_watchlist="", id_utilisateur=0, id_watchlist=id_watchlist)
        films = service_watchlist.sauvegarder_watchlist(watchlist)
<<<<<<< HEAD
        return {"films": films}

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur interne du serveur.")
=======

        logger.info(f"Récupération des films pour la watchlist {id_watchlist} réussie.")
        return {"films": films}

    except ValueError as e:
        logger.error(f"Erreur de valeur lors de la récupération des films : {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception(
            f"Erreur interne lors de la récupération des films de la watchlist : {e}"
        )
        raise HTTPException(status_code=500, detail="Erreur interne du serveur.")

>>>>>>> a73b05db2e8e2645eb8c912745b3cb85574b99eb

@router.get("/watchlists/utilisateur/{id_utilisateur}", response_model=dict)
async def afficher_watchlist(id_utilisateur: int):
    """
    Récupère toutes les watchlists d'un utilisateur spécifique, avec les films associés.
    """
    try:
        utilisateur = utilisateur_dao.trouver_par_id(id_utilisateur)
        if not utilisateur:
<<<<<<< HEAD
=======
            logger.warning(f"Utilisateur avec id {id_utilisateur} introuvable.")
>>>>>>> a73b05db2e8e2645eb8c912745b3cb85574b99eb
            raise HTTPException(status_code=404, detail="Utilisateur introuvable.")

        watchlists = service_watchlist.afficher_watchlist(id_utilisateur)
<<<<<<< HEAD
        return {"watchlists": watchlists}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
=======

        # Étape 3 : Retourner les watchlists et leurs films associés
        logger.info(f"Watchlists récupérées pour l'utilisateur {id_utilisateur}.")
        return {"watchlists": watchlists}

    except ValueError as e:
        logger.error(f"Erreur de valeur lors de la récupération des watchlists : {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(f"Erreur interne lors de la récupération des watchlists : {e}")
>>>>>>> a73b05db2e8e2645eb8c912745b3cb85574b99eb
        raise HTTPException(status_code=500, detail="Erreur interne du serveur.")
