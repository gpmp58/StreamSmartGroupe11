from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from src.webservice.services.service_watchlist import WatchlistService
from src.webservice.business_object.watchlist import Watchlist
from src.webservice.business_object.film import Film
from src.webservice.dao.watchlist_dao import WatchlistDao

# Création du router FastAPI
router = APIRouter()

pass