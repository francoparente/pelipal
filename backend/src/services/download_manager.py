import requests
import subprocess
import os

class DownloadManager:
    BASE_URL = "https://yts.mx/api/v2"
    DOWNLOAD_PATH = "downloads"

    def __init__(self):
        os.makedirs(self.DOWNLOAD_PATH, exist_ok=True)

    def search_movie(self, query: str):
        """Busca una película en YTS y devuelve los resultados."""
        response = requests.get(f"{self.BASE_URL}/list_movies.json", params={"query_term": query})
        return response.json()

    def download_torrent(self, torrent_url: str):
        """Descarga y ejecuta un torrent con aria2c."""
        torrent_path = os.path.join(self.DOWNLOAD_PATH, "movie.torrent")

        # Descarga el archivo .torrent
        response = requests.get(torrent_url, stream=True)
        with open(torrent_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        # Ejecuta aria2c para descargar la película
        subprocess.Popen(["aria2c", "--dir=" + self.DOWNLOAD_PATH, torrent_path])

        return {"message": "Descarga iniciada", "file_path": torrent_path}
