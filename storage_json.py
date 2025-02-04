import json
from istorage import IStorage


class StorageJson(IStorage):
    """
    A storage implementation using JSON file to store and manage movie data.

    Args:
    file_path (str): The file path for the JSON file used for storing movie data.

    Methods:
    - _load_data: Loads movie data from the JSON file.
    - _save_data: Saves movie data to the JSON file.
    - list_movies: Returns a list of all movies in the storage.
    - add_movie: Adds a new movie to the storage.
    - delete_movie: Deletes a specific movie from the storage.
    - update_movie: Updates the rating of a specific movie in the storage.
    """
    def __init__(self, file_path):
        """
        Initializes a new instance of the class.

        Args:
        file_path (str): The file path for the JSON file used for storing movie data.

        Returns:
        None
        """
        self.file_path = file_path
        self.movies = {}
        self._load_data()


    def _load_data(self):
        """
        Loads movie data from the JSON file.

        Returns:
        None
        """
        try:
            with open(self.file_path, 'r') as file:
                self.movies = json.load(file)
        except FileNotFoundError:
            # If the file does not exist, initialize an empty dictionary for movies
            self.movies = {}


    def _save_data(self):
        """
        Saves movie data to the JSON file.

        Returns:
        None
        """
        with open(self.file_path, 'w') as file:
            json.dump(self.movies, file, indent=4)


    def list_movies(self):
        """
        Returns a dict of all movies in the storage.

        Returns:
        dict: A dict of all movies in the storage.
        """
        return self.movies


    def add_movie(self, title, year, rating, poster, plot, genre, director):
        """
        Adds a new movie to the storage.

        Args:
        title (str): The title of the movie.
        year (str): The year of release of the movie.
        rating (float): The rating of the movie.
        poster (str): The URL of the movie poster.
        plot (str): The plot summary of the movie.
        genre (str): The genre of the movie.
        director (str): The director of the movie.

        Returns:
        None
        """
        new_movie = {
            "year_of_release": year,
            "rating": rating,
            "poster": poster,
            "plot": plot,
            "genre": genre,
            "director": director
            }
        self.movies[title] = new_movie
        self._save_data()


    @staticmethod
    def is_exist(title, movies_dict):
        for movie in movies_dict:
            if title.lower() in movie.lower():
                return (True, movie)
        return (False, title)


    def delete_movie(self, title):
        """
        Deletes a specific movie from the storage.

        Args:
        title (str): The title of the movie to be deleted.

        Returns:
        None
        """
        movie_exist = self.is_exist(title, self.movies)
        if movie_exist[0]:
            del self.movies[movie_exist[1]]
            print(f"Movie with title '{title}' was successfully deleted.")
        else:
                print(f"Movie with title '{title}' not found.")
        self._save_data()


    def update_movie(self, title, rating):
        """
        Updates the rating of a specific movie in the storage.

        Args:
        title (str): The title of the movie to be updated.
        rating (float): The new rating of the movie.

        Returns:
        None
        """
        if title in self.movies:
            self.movies[title]["rating"] = rating
            self._save_data()
        else:
            print(f"Movie with title '{title}' not found.")
