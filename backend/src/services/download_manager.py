import requests
import subprocess
import os

class DownloadManagerService:
    DOWNLOAD_PATH = "/mnt/e/Videos/Movies"

    def __init__(self):
        os.makedirs(self.DOWNLOAD_PATH, exist_ok=True)

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
