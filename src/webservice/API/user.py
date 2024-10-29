from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.webservice.business_object.utilisateur import Utilisateur
from src.webservice.services.service_utilisateur import UtilisateurService
from src.webservice.dao.utilisateur_dao import UtilisateurDAO

# Création du router FastAPI
router = APIRouter()

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

# Modèle de données pour afficher les informations d'un utilisateur sans le mot de passe
class UtilisateurDisplayModel(BaseModel):
    nom: str
    prenom: str
    pseudo: str
    adresse_mail: str
    langue: str

# 1. POST /utilisateurs : Créer un nouvel utilisateur
@router.post("/utilisateurs", response_model=UtilisateurDisplayModel)
async def create_utilisateur(utilisateur: UtilisateurModel):
    """
    Crée un nouvel utilisateur dans la base de données.
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
            return UtilisateurDisplayModel(
                nom=nouvel_utilisateur.nom,
                prenom=nouvel_utilisateur.prenom,
                pseudo=nouvel_utilisateur.pseudo,
                adresse_mail=nouvel_utilisateur.adresse_mail,
                langue=nouvel_utilisateur.langue,
            )
        else:
            raise HTTPException(
                status_code=400, detail="Erreur lors de la création de l'utilisateur."
            )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# 2. DELETE /utilisateurs/{id_utilisateur} : Supprimer un utilisateur
@router.delete("/utilisateurs/{id_utilisateur}")
async def delete_utilisateur(id_utilisateur: str):
    """
    Supprime un utilisateur basé sur son identifiant.
    """
    try:
        utilisateur_service.supprimer_compte(id_utilisateur=id_utilisateur)
        return {"message": f"Utilisateur avec id '{id_utilisateur}' supprimé avec succès"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# 3. POST /utilisateurs/login : Connexion d'un utilisateur
class LoginModel(BaseModel):
    pseudo: str
    mdp: str

@router.post("/utilisateurs/login")
async def login_utilisateur(credentials: LoginModel):
    """
    Permet à un utilisateur de se connecter.
    """
    try:
        message = utilisateur_service.se_connecter(pseudo=credentials.pseudo, mdp=credentials.mdp)
        return {"message": message}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# 4. GET /utilisateurs/{id_utilisateur}/afficher : Afficher les infos d'un utilisateur
@router.get("/utilisateurs/{id_utilisateur}/afficher", response_model=UtilisateurDisplayModel)
async def afficher_utilisateur(id_utilisateur: str):
    """
    Affiche les informations d'un utilisateur basé sur son id.
    """
    try:
        utilisateur_info = utilisateur_service.afficher(id_utilisateur=id_utilisateur)

        # Construire le modèle de réponse à partir de l'utilisateur récupéré
        return UtilisateurDisplayModel(
            nom=utilisateur_info["Nom"],
            prenom=utilisateur_info["Prénom"],
            pseudo=utilisateur_info["Pseudo"],
            adresse_mail=utilisateur_info["Adresse mail"],
            langue=utilisateur_info["Langue"],
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
