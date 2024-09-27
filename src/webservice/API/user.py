from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

# Exemple de bdd d'utilisateurs
utilisateurs_db = [
    {"pseudo": "user1", "nom": "Dupont", "prenom": "Alice", "adresse_mail": "alice@example.com", "mdp": "password123"},
    {"pseudo": "user2", "nom": "Martin", "prenom": "Bob", "adresse_mail": "bob@example.com", "mdp": "password456"},
    {"pseudo": "user3", "nom": "Leroy", "prenom": "Charlie", "adresse_mail": "charlie@example.com", "mdp": "password789"}
]


# Modèle de données pour un utilisateur
class utilisateur(BaseModel):
    pseudo : str
    nom : str
    prenom : str
    adresse_mail : str
    mdp : str

# 1. GET /utilisateurs : Récupérer tous les utilisateurs
@router.get("/utilisateurs", response_model=List[utilisateur])
async def get_utilisateurs():
    return utilisateurs_db

# 2. GET /utilisateurs/{pseudo} : Récupérer un utilisateur spécifique
@router.get("/utilisateurs/{utilisateur_pseudo}", response_model=utilisateur)
async def get_utilisateur(utilisateur_pseudo: str):
    utilisateur = next((utilisateur for utilisateur in utilisateurs_db if utilisateur["pseudo"] == utilisateur_pseudo), None)
    if utilisateur:
        return utilisateur
    raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

# 3. POST /utilisateurs : Créer un nouvel utilisateur
@router.post("/utilisateurs", response_model=utilisateur)
async def create_utilisateur(utilisateur: utilisateur):
    utilisateur.pseudo = len(utilisateurs_db) + 1  # Générer un nouvel pseudo pour l'utilisateur
    utilisateurs_db.append(utilisateur.dict())  # Ajouter l'utilisateur à la base de données
    return utilisateur

# 4. PUT /utilisateurs/{pseudo} : Mettre à jour un utilisateur existant
@router.put("/utilisateurs/{utilisateur_pseudo}", response_model=utilisateur)
async def update_utilisateur(utilisateur_pseudo: int, updated_utilisateur: utilisateur):
    utilisateur = next((utilisateur for utilisateur in utilisateurs_db if utilisateur["pseudo"] == utilisateur_pseudo), None)
    if utilisateur:
        utilisateur.update(updated_utilisateur.dict())  # Mise à jour des champs de l'utilisateur
        return utilisateur
    raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

# 5. DELETE /utilisateurs/{pseudo} : Supprimer un utilisateur
@router.delete("/utilisateurs/{utilisateur_pseudo}")
async def delete_utilisateur(utilisateur_pseudo: int):
    global utilisateurs_db
    utilisateur = next((utilisateur for utilisateur in utilisateurs_db if utilisateur["pseudo"] == utilisateur_pseudo), None)
    if utilisateur:
        utilisateurs_db = [u for u in utilisateurs_db if u["pseudo"] != utilisateur_pseudo]  # Supprimer l'utilisateur
        return {"message": "Utilisateur supprimé avec succès"}
    raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
