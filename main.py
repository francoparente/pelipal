from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.src.routers import movies
from backend.src.services.movie_search import MovieSearchService
from backend.src.services.download_manager import DownloadManagerService
from backend.src.services.ratings import RatingsService
from backend.src.services.series_chart import SeriesChartService
from backend.src.routers.movies import router as movies_router
# from backend.src.routers.ratings import router as ratings_router
# from backend.src.routers.series import router as series_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://192.168.0.159:5173"],  # Permite solicitudes desde el frontend
    allow_origins=["*"],  # Allow requests from any origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(movies.router)
# app.include_router(ratings_router, prefix="/api/ratings", tags=["ratings"])
# app.include_router(series_router, prefix="/api/series", tags=["series"])

