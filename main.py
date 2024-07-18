from storage_json import StorageJson
from movie_app import MovieApp


def main():
    """
    The main function for the movie application.
    
    Creates a StorageJson instance with the filename "data.json",
    creates a MovieApp instance using the created StorageJson instance,
    and then calls the run method to start the movie application.
    """
    storage = StorageJson("data.json")
    movies = MovieApp(storage)
    movies.run()


if __name__ == "__main__":
    main()
