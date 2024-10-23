from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from src.webservice.business_object.utilisateur import Utilisateur
from src.webservice.services.service_utilisateur import UtilisateurService
from src.webservice.dao.utilisateur_dao import UtilisateurDAO

# Création du router FastAPI
router = APIRouter()
router.include_router(router)

# Initialisation du service utilisateur
utilisateur_dao = UtilisateurDAO()
utilisateur_service = UtilisateurService(utilisateur=utilisateur_dao)


# Modèle de données pour un utilisateur (utilisé pour l'API)
class UtilisateurModel(BaseModel):
    nom: str
    prenom: str
    pseudo: str
    adresse_mail: str
    mdp: str
    langue: str = "français"


# 1. POST /utilisateurs : Créer un nouvel utilisateur
@router.post("/utilisateurs", response_model=UtilisateurModel)
async def create_utilisateur(utilisateur: UtilisateurModel):
    """
    Crée un nouvel utilisateur dans la base de données.

    Paramètres:
    ------------
    utilisateur : UtilisateurModel
        Les informations du nouvel utilisateur.

    Returns:
    ---------
    UtilisateurModel : L'utilisateur créé avec succès.
    """
    try:
        nouvel_utilisateur = utilisateur_service.creer_compte(
            nom=utilisateur.nom,
            prenom=utilisateur.prenom,
            pseudo=utilisateur.pseudo,
            adresse_mail=utilisateur.adresse_mail,
            mdp=utilisateur.mdp,
            langue=utilisateur.langue,
        )
        # Si la création est réussie, retourner l'objet Utilisateur
        if isinstance(nouvel_utilisateur, Utilisateur):
            return UtilisateurModel(
                nom=nouvel_utilisateur.nom,
                prenom=nouvel_utilisateur.prenom,
                pseudo=nouvel_utilisateur.pseudo,
                adresse_mail=nouvel_utilisateur.adresse_mail,
                mdp=nouvel_utilisateur.mdp,
                langue=nouvel_utilisateur.langue,
            )
        else:
            raise HTTPException(
                status_code=400, detail="Erreur lors de la création de l'utilisateur."
            )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# 2. DELETE /utilisateurs/{pseudo} : Supprimer un utilisateur
@router.delete("/utilisateurs/{pseudo}")
async def delete_utilisateur(pseudo: str):
    """
    Supprime un utilisateur basé sur son pseudo.

    Paramètres:
    ------------
    pseudo : str
        Le pseudo de l'utilisateur à supprimer.

    Returns:
    ---------
    dict : Message confirmant la suppression.
    """
    try:
        utilisateur_service.supprimer_compte(pseudo_utilisateur=pseudo)
        return {"message": f"Utilisateur '{pseudo}' supprimé avec succès"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# 3. POST /utilisateurs/login : Connexion d'un utilisateur
@router.post("/utilisateurs/login")
async def login_utilisateur(pseudo: str, mdp: str):
    """
    Permet à un utilisateur de se connecter.

    Paramètres:
    ------------
    pseudo : str
        Le pseudo de l'utilisateur.
    mdp : str
        Le mot de passe de l'utilisateur.

    Returns:
    ---------
    dict : Message de bienvenue si les identifiants sont corrects.
    """
    try:
        message = utilisateur_service.se_connecter(pseudo=pseudo, mdp=mdp)
        return {"message": message}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# 4. GET /utilisateurs/{id_utilisateur}/afficher : Afficher les infos d'un utilisateur
@router.get("/utilisateurs/{id_utilisateur}/afficher", response_model=UtilisateurModel)
async def afficher_utilisateur(id_utilisateur: str):
    """
    Affiche les informations d'un utilisateur basé sur son id.

    Paramètres:
    ------------
    id_utilisateur : str
        L'identifiant de l'utilisateur dont on veut afficher les informations.

    Returns:
    ---------
    UtilisateurModel : Informations de l'utilisateur.
    """
    try:
        # Utiliser la méthode `afficher` pour obtenir les informations de l'utilisateur
        utilisateur_info = utilisateur_service.afficher(id_utilisateur=id_utilisateur)

        # Construire le modèle de réponse à partir de l'utilisateur récupéré
        return UtilisateurModel(
            nom=utilisateur_info["nom"],
            prenom=utilisateur_info["prenom"],
            pseudo=utilisateur_info["pseudo"],
            adresse_mail=utilisateur_info["adresse_mail"],
            mdp=utilisateur_info["mdp"],
            langue=utilisateur_info["langue"],
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
