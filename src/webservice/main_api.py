# src/webservice/main_api.py

import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.webservice.API import user, movie, watchlist

# Configuration du logging
logging.basicConfig(
    level=logging.DEBUG,  # Niveau de log
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()  # Affiche les logs dans la console
    ]
)

logger = logging.getLogger("watchlist_api")

app = FastAPI()

# Inclure les routes
app.include_router(user.router)
app.include_router(movie.router)
app.include_router(watchlist.router)

# Gestionnaire d'exception global
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Erreur interne du serveur."},
    )
