from abc import ABC, abstractmethod

class IStorage(ABC):
    """An abstract base class representing a storage interface for movies."""

    @abstractmethod
    def list_movies(self):
        """Retrieve a list of all movies stored in the storage.

        Returns:
        list: A list of all movies stored in the storage.
        """
        pass


    @abstractmethod
    def add_movie(self, title, year, rating, poster):
        """Add a new movie to the storage.

        Args:
        title (str): The title of the movie.
        year (int): The release year of the movie.
        rating (float): The rating of the movie.
        poster (str): The URL of the movie's poster.

        Returns:
        bool: True if the movie is successfully added, otherwise False.
        """
        pass


    @abstractmethod
    def delete_movie(self, title):
        """Delete a movie from the storage.

        Args:
        title (str): The title of the movie to be deleted.

        Returns:
        bool: True if the movie is successfully deleted, otherwise False.
        """
        pass


    @abstractmethod
    def update_movie(self, title, rating):
        """Update the rating of a movie in the storage.

        Args:
        title (str): The title of the movie to be updated.
        rating (float): The new rating of the movie.

        Returns:
        bool: True if the movie is successfully updated, otherwise False.
        """
        pass