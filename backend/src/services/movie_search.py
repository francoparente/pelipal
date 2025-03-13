import os
import requests

class MovieSearchService:
    BASE_URL = "https://yts.mx/api/v2"

    def __init__(self, hdd_path="/mnt/e/Videos/Movies"):
        self.hdd_path = hdd_path

    def search_in_hdd(self, movie_title: str):
        """
        if not movie_title:
            return []
        matching_movies = []

        Parameters:
        movie_title (str): The title of the movie to search for.

        Returns:
        list: A list of file paths that match the movie title. Returns an empty list if no matches are found.
        """
        if not movie_title:
            return []
        matching_movies = []
        words = movie_title.split()
        for root, dirs, files in os.walk(self.hdd_path):
            for filename in files:
                if all(word.lower() in filename.lower() for word in words):
                    matching_movies.append(os.path.join(root, filename))
        return matching_movies

    def search_in_yts(self, movie_title: str):
        """
        Searches for a movie on the YTS website using the provided title.

        Parameters:
        movie_title (str): The title of the movie to search for.

        Returns:
        dict: A dictionary containing the JSON response from the YTS API, which includes movie details if found.
        """
        try:
            response = requests.get(f"{self.BASE_URL}/list_movies.json",
                                    params={"query_term": movie_title})
            response.raise_for_status()  # Raise an HTTPError for bad responses
            return response.json()
        except requests.exceptions.RequestException as e:
            # Log the error or handle it as needed
            print(f"An error occurred: {e}")
            return None  # or raise a custom exception
    
    def search_movie(self, movie_title: str):
        """
        Searches for a movie by title in both the local HDD and the YTS website.

        Parameters:
        movie_title (str): The title of the movie to search for.

        Returns:
        dict: A dictionary indicating the source of the movie and the corresponding data.
              If found on the HDD, returns {"source": "HDD", "path": list_of_file_paths}.
              If found on YTS, returns {"source": "YTS", "data": yts_response_data}.
              Returns None if the movie is not found in either source.
        """
        hdd_result = self.search_in_hdd(movie_title)
        if hdd_result:
            return {"source": "HDD", "path": hdd_result}

        yts_result = self.search_in_yts(movie_title)
        if yts_result:
            return {"source": "YTS", "data": yts_result}

        return None
