from fastapi import FastAPI
from backend.src.routers import movies
from backend.src.services.movie_search import MovieSearchService
from backend.src.services.download_manager import DownloadManagerService
from backend.src.services.ratings import RatingsService
from backend.src.services.series_chart import SeriesChartService
from backend.src.routers.movies import router as movies_router
# from backend.src.routers.ratings import router as ratings_router
# from backend.src.routers.series import router as series_router


app = FastAPI()
app.include_router(movies.router)

app.include_router(movies_router, prefix="/api/movies", tags=["movies"])
# app.include_router(ratings_router, prefix="/api/ratings", tags=["ratings"])
# app.include_router(series_router, prefix="/api/series", tags=["series"])

