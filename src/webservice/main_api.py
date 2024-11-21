from fastapi import FastAPI
import uvicorn

from src.webservice.API import user, movie, watchlist, plateforme, critere

app = FastAPI()

app.include_router(user.router)
app.include_router(movie.router)
app.include_router(watchlist.router)
app.include_router(plateforme.router)
app.include_router(critere.router)

uvicorn.run(app, host="0.0.0.0", port=8000)

"""
Lien d'accès au Swagger : http://127.0.0.1:8000/docs

"""
