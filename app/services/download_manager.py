import requests

class DownloadManager:
    BASE_URL = "https://yts.mx/api/v2"

    def search_movie(self, query: str):
        """Busca una película en YTS y devuelve los resultados."""
        response = requests.get(f"{self.BASE_URL}/list_movies.json", params={"query_term": query})
        return response.json()

    def download_torrent(self, torrent_url: str, download_path: str):
        """Descarga un archivo torrent."""
        response = requests.get(torrent_url, stream=True)
        file_path = f"{download_path}/movie.torrent"

        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return file_path
