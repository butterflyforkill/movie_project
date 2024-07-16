import json
from istorage import IStorage


class StorageJson(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path


    def list_movies(self):
        with open('data.json', 'r') as file:
            movies = json.load(file)
        return movies


    def add_movie(self, title, year, rating, poster, plot, genre, director):
        all_movies = self.list_movies()
        new_movie = {
            "year_of_release": year,
            "rating": rating,
            "poster": poster,
            "plot": plot,
            "genre": genre,
            "director": director
            }
        all_movies[title] = new_movie
        self._save_data(all_movies)
        return True


    def delete_movie(self, title):
        all_movies = self.list_movies()
        if title in all_movies:
            del all_movies[title]
        else:
            return False
        self._save_data(all_movies)
        return True


    def update_movie(self, title, rating):
        movies = self.list_movies()
        for movie in movies:
            if movie['title'] == title:
                movie['rating'] = rating
                break
        self._save_data(movies)
        return True


    def _save_data(self, data):
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)

# storage = StorageJson('data.json')
# print(storage.list_movies())
# storage.add_movie('title', '1934', '9', 'poster', 'plot', 'genre', 'director')
# print(storage.list_movies())
# storage.delete_movie('title')
# print(storage.list_movies())