import os
import sys
from unittest.mock import patch, MagicMock
import pytest

# Explicitly import from services
from services.movie_search import MovieSearchService

# Fixture for the MovieSearchService instance
@pytest.fixture
def movie_search_service():
    """Fixture to provide a MovieSearchService instance."""
    return MovieSearchService("/mnt/e/Videos/Movies")

# Tests for search_in_hdd
def test_search_in_hdd_empty_hdd(movie_search_service):
    """Should return an empty list when the HDD is empty."""
    with patch("os.walk") as mock_walk:
        mock_walk.return_value = []  # Simulate an empty HDD
        result = movie_search_service.search_in_hdd("Inception")
        assert result == []

def test_search_in_hdd_no_matches(movie_search_service):
    """Should return an empty list when no movie matches the title."""
    with patch("os.walk") as mock_walk:
        mock_walk.return_value = [
            (movie_search_service.hdd_path, [], ["The Matrix.mp4", "Interstellar.mp4"])
        ]
        result = movie_search_service.search_in_hdd("Inception")
        assert result == []

def test_search_in_hdd_multiple_matches(movie_search_service):
    """Should return a list of matching movies when the title matches multiple files."""
    with patch("os.walk") as mock_walk:
        mock_walk.return_value = [
            (movie_search_service.hdd_path, [], ["Inception.mp4", "Inception 2.mp4"])
        ]
        result = movie_search_service.search_in_hdd("Inception")
        assert result == [
            os.path.join(movie_search_service.hdd_path, "Inception.mp4"),
            os.path.join(movie_search_service.hdd_path, "Inception 2.mp4"),
        ]

def test_search_in_hdd_single_match(movie_search_service):
    """Should return a list with a single movie when the title matches exactly one file."""
    with patch("os.walk") as mock_walk:
        mock_walk.return_value = [
            (movie_search_service.hdd_path, [], ["Inception.mp4"])
        ]
        result = movie_search_service.search_in_hdd("Inception")
        assert result == [os.path.join(movie_search_service.hdd_path, "Inception.mp4")]

def test_search_in_hdd_case_insensitive(movie_search_service):
    """Should handle case-insensitive matches for movie titles."""
    with patch("os.walk") as mock_walk:
        mock_walk.return_value = [
            (movie_search_service.hdd_path, [], ["inception.mp4"])
        ]
        result = movie_search_service.search_in_hdd("InCePtIoN")
        assert result == [os.path.join(movie_search_service.hdd_path, "inception.mp4")]

def test_search_in_hdd_empty_title(movie_search_service):
    """Should return an empty list when the movie title is an empty string."""
    with patch("os.walk") as mock_walk:
        mock_walk.return_value = [
            (movie_search_service.hdd_path, [], ["Inception.mp4"])
        ]
        result = movie_search_service.search_in_hdd("")
        assert result == []

def test_search_in_hdd_special_characters(movie_search_service):
    """Should correctly match movie titles with special characters."""
    with patch("os.walk") as mock_walk:
        mock_walk.return_value = [
            (movie_search_service.hdd_path, [], ["Inception: Part 1.mp4"])
        ]
        result = movie_search_service.search_in_hdd("Inception: Part 1")
        assert result == [os.path.join(movie_search_service.hdd_path, "Inception: Part 1.mp4")]

def test_search_in_hdd_numbers_in_title(movie_search_service):
    """Should correctly match movie titles with numbers in their names."""
    with patch("os.walk") as mock_walk:
        mock_walk.return_value = [
            (movie_search_service.hdd_path, [], ["Inception 2.mp4"])
        ]
        result = movie_search_service.search_in_hdd("Inception 2")
        assert result == [os.path.join(movie_search_service.hdd_path, "Inception 2.mp4")]

def test_search_in_hdd_long_title(movie_search_service):
    """Should handle very long movie titles without errors."""
    long_title = "A" * 1000  # A very long title
    with patch("os.walk") as mock_walk:
        mock_walk.return_value = [
            (movie_search_service.hdd_path, [], [f"{long_title}.mp4"])
        ]
        result = movie_search_service.search_in_hdd(long_title)
        assert result == [os.path.join(movie_search_service.hdd_path, f"{long_title}.mp4")]

def test_search_in_hdd_deeply_nested_directories(movie_search_service):
    """Should correctly match movie titles when the HDD contains deeply nested directories."""
    nested_path = os.path.join(movie_search_service.hdd_path, "dir1", "dir2", "dir3")
    with patch("os.walk") as mock_walk:
        mock_walk.return_value = [
            (nested_path, [], ["Inception.mp4"])
        ]
        result = movie_search_service.search_in_hdd("Inception")
        assert result == [os.path.join(nested_path, "Inception.mp4")]

# Tests for search_in_yts
def test_search_in_yts(movie_search_service):
    """Should return the correct JSON response from YTS."""
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": {"movies": [{"title": "Inception"}]}}
        mock_get.return_value = mock_response

        result = movie_search_service.search_in_yts("Inception")
        assert result == {"data": {"movies": [{"title": "Inception"}]}}
        mock_get.assert_called_once_with(
            f"{movie_search_service.BASE_URL}/list_movies.json",
            params={"query_term": "Inception"},
        )

# Tests for search_movie
def test_search_movie_hdd_match(movie_search_service):
    """Should return HDD results if a match is found in the HDD."""
    with patch("os.walk") as mock_walk, patch("requests.get") as mock_get:
        mock_walk.return_value = [
            (movie_search_service.hdd_path, [], ["Inception.mp4"])
        ]
        result = movie_search_service.search_movie("Inception")
        assert result == {"source": "HDD", "path": [os.path.join(movie_search_service.hdd_path, "Inception.mp4")]}
        mock_get.assert_not_called()  # Ensure YTS is not called

def test_search_movie_yts_match(movie_search_service):
    """Should return YTS results if no match is found in the HDD."""
    with patch("os.walk") as mock_walk, patch("requests.get") as mock_get:
        mock_walk.return_value = []  # No matches in HDD
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": {"movies": [{"title": "Inception"}]}}
        mock_get.return_value = mock_response

        result = movie_search_service.search_movie("Inception")
        assert result == {"source": "YTS", "data": {"data": {"movies": [{"title": "Inception"}]}}}
        mock_get.assert_called_once_with(
            f"{movie_search_service.BASE_URL}/list_movies.json",
            params={"query_term": "Inception"},
        )

def test_search_movie_no_match(movie_search_service):
    """Should return None if no match is found in the HDD or YTS."""
    with patch("os.walk") as mock_walk, patch("requests.get") as mock_get:
        mock_walk.return_value = []  # No matches in HDD
        mock_response = MagicMock()
        mock_response.json.return_value = {}  # No matches in YTS
        mock_get.return_value = mock_response

        result = movie_search_service.search_movie("Inception")
        assert result is None
        mock_get.assert_called_once_with(
            f"{movie_search_service.BASE_URL}/list_movies.json",
            params={"query_term": "Inception"},
        )