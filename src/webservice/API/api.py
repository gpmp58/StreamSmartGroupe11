from fastapi import Body, FastAPI
import os
from dotenv import load_dotenv
import requests
import json
from pydantic import BaseModel, Field
from services.service_utilisateur import UtilisateurService

load_dotenv()

cle_api = os.environ.get("API_KEY")

#uvicorn api:app --reload
app = FastAPI()


@app.get("/rechercher_film/{name}")
async def get_providers_for_movie_api(name):
    return get_providers_for_movie(movie_name=name)


class User(BaseModel):
    name: str
    password: str


@app.post("/create_user")
async def update_item(user: User):
    return user

@app.get("/connexion_user")
async def connexion(adresse_mail,mdp):
    return service_utilisateur.se_connecter(adresse_mail,mdp)
