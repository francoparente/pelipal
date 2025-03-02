from fastapi import APIRouter
from app.services.download_manager import DownloadManager

router = APIRouter()
download_manager = DownloadManager()

@router.get("/movies/search")
def search_movies(query: str):
    return download_manager.search_movie(query)

@router.get("/movies/download")
def download_movie(torrent_url: str):
    return download_manager.download_torrent(torrent_url)
