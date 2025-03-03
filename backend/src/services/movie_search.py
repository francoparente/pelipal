import os
import requests

class MovieSearchService:
    BASE_URL = "https://yts.mx/api/v2"

    def __init__(self, hdd_path="/mnt/e/Videos/Movies"):
        self.hdd_path = hdd_path

    def search_in_hdd(self, movie_title: str):
        """Busca una película en el HDD."""
        matching_movies = []
        words = movie_title.split()
        for root, dirs, files in os.walk(self.hdd_path):
            for filename in files:
                if all(word.lower() in filename.lower() for word in words):
                    matching_movies.append(os.path.join(root, filename))
        return matching_movies

    def search_in_yts(self, movie_title: str):
        """Busca una película en YTS y devuelve los resultados."""
        response = requests.get(f"{self.BASE_URL}/list_movies.json",
                                params={"query_term": movie_title})
        return response.json()

    def search_movie(self, movie_title: str):
        """Busca una película en el HDD y, si no la encuentra, en YTS."""
        hdd_result = self.search_in_hdd(movie_title)
        if hdd_result:
            return {"source": "HDD", "path": hdd_result}
        yts_result = self.search_in_yts(movie_title)
        if yts_result:
            return {"source": "YTS", "data": yts_result}
        return None
