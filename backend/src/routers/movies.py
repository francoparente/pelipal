from fastapi import APIRouter
from backend.src.services.download_manager import DownloadManagerService
from backend.src.services.movie_search import MovieSearchService

router = APIRouter()
downloader = DownloadManagerService()
searcher = MovieSearchService()

@router.get("/movies/search")
def search_movies(movie_title: str):
    return searcher.search_movie(movie_title)

@router.get("/movies/download")
def download_movie(torrent_url: str):
    return downloader.download_torrent(torrent_url)