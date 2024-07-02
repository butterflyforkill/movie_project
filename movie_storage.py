import json


def get_movies():
    """
    Returns a dictionary of dictionaries that
    contains the movies information in the database.

    The function loads the information from the JSON
    file and returns the data. 

    For example, the function may return:
    {
      "Titanic": {
        "rating": 9,
        "year": 1999
      },
      "..." {
        ...
      },
    }
    """
    with open('data.json', 'r') as file:
        movies = json.load(file)
    return movies


def save_movies(movies):
    """
    Gets all your movies as an argument and saves them to the JSON file.
    """
    with open('data.json', 'w') as file:
        json.dump(movies, file)


def add_movie(title, year, rating, poster):
    """
    Adds a movie to the movies database.
    Loads the information from the JSON file, add the movie,
    and saves it. The function doesn't need to validate the input.
    """
    all_movies = get_movies()
   
    new_movie = {
      "year_of_release": year,
      "rating": rating,
      "poster": poster
    }
    all_movies[title] = new_movie
    save_movies(all_movies)


def delete_movie(title):
    """
    Deletes a movie from the movies database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    all_movies = get_movies()
    if title in all_movies:
        del all_movies[title]
        print(f"Movie {title} successfully deleted")
    else:
        print("Movie not found in the library")
    save_movies(all_movies)


def update_movie(title, notes):
    """
    Updates a movie from the movies database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    all_movies = get_movies()
    if title in all_movies:
        all_movies[title]["notes"] = notes
        print(f"Movie {title} successfully updated. The notes was added.")
    else:
        print(f"ERROR: {title} doesn't exist in the library")
    save_movies(all_movies)
    