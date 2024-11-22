from fastapi import FastAPI
import uvicorn

from src.webservice.API import user, movie, watchlist, plateforme, critere

app = FastAPI()

app.include_router(user.router)
app.include_router(movie.router)
app.include_router(watchlist.router)
app.include_router(plateforme.router)
app.include_router(critere.router)

if __name__ == "__main__":
    uvicorn.run(
        "main_api:app",
        host="0.0.0.0",
        port=8000,
        log_level="critical",  # Réduit les logs à seulement les erreurs critiques
        access_log=False,      # Désactive les logs d'accès (requêtes HTTP)
        reload=True            # Optionnel : recharge automatique pour le développement
    )

"""
Lien d'accès au Swagger : http://127.0.0.1:8000/docs
"""
