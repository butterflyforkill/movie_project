import random
import sys
import matplotlib.pyplot as plt
import requests
import docs_parcer
from config.config_files import APIkeys
from storage_csv import StorageCsv

INDEX_HTML_PATH = '_static/index_template.html'
MOVIE_HTML_PATH = '_static/movie_template.html'


class MovieApp:
    """
    Represents a movie application with various functionalities for managing and interacting with movie data.

    Attributes:
    _storage: The storage object used for storing and retrieving movie data.

    Methods:
    - _command_list_movies: Displays the list of movies along with their ratings and year of release from the storage.
    - response_parser: Parses the response from an HTTP request and returns the appropriate data or error message.
    - _command_add_movie: Allows the user to add a new movie to the storage using the OMDB API.
    - _command_delete_movie: Allows the user to delete a specific movie from the storage.
    - _command_update_movie: Allows the user to update the rating or notes for a specific movie.
    - _command_random_movie: Retrieves the movie data from the storage and selects a random movie to watch for the night.
    - _command_search: Retrieves the movie data from the storage and searches for movies based on a partial match of the movie name.
    - _command_sorted_movies: Retrieves the movie data from the storage and prints the movies sorted by their ratings in descending order.
    - _command_movie_stats: Computes and prints various statistics based on the movie data obtained from the storage.
    - _command_creating_histogram: Creates a histogram based on the ratings of the movies obtained from the storage.
    - generate_movie_page: Generates individual HTML pages for each movie based on the movie data stored in the movie storage.
    - _generate_website: Generate a website based on the movie data.
    - exit_program: Exit the program.
    - get_user_input: Get user input for menu options and validate the input.
    - display_menu: Display the menu options for the program.
    - run: Main function to run the program and interact with the user.
    """
    def __init__(self, storage):
        """
        Initializes a new instance of the class.

        Args:
        storage: The storage object to be used for storing and retrieving movie data.

        Returns:
        None
        """
        self._storage = storage


    def _command_list_movies(self):
        """
        Displays the list of movies along with their ratings and year of release from the storage.

        Retrieves the list of movies and their details from the storage and prints the total number of movies. Then, 
        iterates through the movies and prints each movie's name, rating, and year of release.

        Returns:
            None
        """
        movies_data = self._storage.list_movies()
        length = len(movies_data)
        print(f"\n{length} movies in total\n")
        for movie_name, movie_data in movies_data.items():
            print(f"{movie_name}: {movie_data['rating']}", 
                f"{movie_data['year_of_release']}")

    @staticmethod
    def response_parser(resp):
        """
        Parses the response from an HTTP request and
        returns the appropriate data or error message.

        Args:
        resp (requests.Response): The response object
            from the HTTP request.

        Returns:
        dict or str: If the response status code is OK
                    and the JSON response indicates success,
                    returns the JSON data.
                    If the JSON response indicates failure,
                    returns an error message.
                    If the response status code is not OK,
                    returns an error message with the status code.
        """
        if resp.status_code == requests.codes.ok:
            if resp.json()['Response'] == 'False':
                error_resp = resp.json()
                return f"Error: {error_resp['Error']}"
            else:
                return resp.json()
        else:
            return f"Error: {resp.status_code}"


    def _command_add_movie(self):
        """
        Allows the user to add a new movie to the storage using the OMDB API.

        Prompts the user to enter the name of the new movie. Checks if the movie already exists in the storage. If the movie
        exists, it notifies the user; if not, it fetches details about the movie using the OMDB API, parses the response,
        and then adds the movie along with its details to the storage.

        Returns:
            None
        """
        movie = input("Enter new movie name: ")
        all_movies = self._storage.list_movies()
        if movie in all_movies:
            print(f"Movie {movie} already exist!")
            return
        api_url = f'http://www.omdbapi.com/?apikey={APIkeys.APIkey}&t={movie}'
        response = requests.get(api_url)
        parsed_resp = self.response_parser(response)
        if parsed_resp == 'Error: Movie not found!':
            print(f"The movie {movie} doesn't exist")
        elif type(parsed_resp) == str:
            print(parsed_resp)
        else:
            rating = float(parsed_resp['Ratings'][0]['Value'].split('/')[0])
            year_str = parsed_resp['Year'] 
            year = year_str[0:4]
            print(rating)
            self._storage.add_movie(
                parsed_resp['Title'],
                year, 
                rating, 
                parsed_resp['Poster'],
                parsed_resp['Plot'],
                parsed_resp['Genre'],
                parsed_resp['Director']
                )
            print(f"Movie {movie} successfully added")


    def _command_delete_movie(self):
        """
        Allows the user to delete a specific movie from the storage.

        Prompts the user to enter the name of the movie to be deleted. The provided movie name is then passed to the storage
        for deletion.

        Returns:
            None
        """
        movie = input("Enter movie name to delete: ")
        self._storage.delete_movie(movie)


    def _command_update_movie(self):
        """
        Allows the user to update the rating or notes for a specific movie.

        Prompts the user to enter the movie name and its updated rating or notes. The provided movie name and the associated
        rating or notes are then passed to the storage for updating.

        Returns:
            None
        """
        movie = input("Enter movie name: ")
        rating = input("Enter movie's new rating: ")
        self._storage.update_movie(movie, rating)


    def _command_random_movie(self):
        """
        Retrieves the movie data from the storage and selects a random movie to watch for the night.

        Fetches the movie data from the storage and randomly selects a movie from the list. The selected movie title and
        its corresponding rating are then printed as a recommendation for the user's movie night.

        Returns:
            None
        """
        movies_data = self._storage.list_movies()
        [random_movie_dict] = random.sample(sorted(movies_data.items()), 1)
        print(f"Your movie for tonight: {random_movie_dict[0]}, "
              f"it's rated {random_movie_dict[1]['rating']}")


    def _command_search(self):
        """
        Retrieves the movie data from the storage and searches for movies based on a partial match of the movie name.

        Retrieves the movie data from the storage and prompts the user to enter a part of a movie name. It then iterates over
        the movie data and checks for a case-insensitive partial match with the entered search term. If a match is found,
        the movie title and its corresponding rating are printed.

        Returns:
            None

        """
        movies_data = self._storage.list_movies()
        search_path = input("Enter part of movie name: ")
        for movie, movie_data in movies_data.items():
            if search_path.lower() in movie.lower():
                print(f"{movie}, {movie_data['rating']}")


    def _command_sorted_movies(self):
        """
        Retrieves the movie data from the storage and prints the movies sorted by their ratings in descending order.

        Fetches the movie data from the storage and sorts the movies based on their ratings in descending order.
        The sorted movies are then iterated over, and for each movie, its title and corresponding rating are printed.

        Returns:
            None

        """
        movies_data = self._storage.list_movies()
        sorted_movies = sorted(movies_data.items(), key=lambda item: item[1]['rating'], reverse=True)
        for movie, details in sorted_movies:
            print(f"{movie}: {details['rating']}")


    def _command_movie_stats(self):
        """
        Computes and prints various statistics based on the movie data obtained from the storage.

        Retrieves the movie data from the storage and calculates the average and median ratings of all
        the movies. The average rating is rounded to two decimal places, and the median rating is
        determined based on the sorted list of all ratings.

        Additionally, the function identifies the best-rated and worst-rated movies by finding the movie
        with the highest and lowest ratings, respectively. The titles and ratings of these movies are then
        printed as part of the statistics.

        Note:
            - If the number of movies is even, the median is calculated as the average of the two middle
            values.
            - If the number of movies is odd, the median is the middle value in the sorted list of ratings.

        Returns:
            None

        """
        movies_data = self._storage.list_movies()
        all_rating = [float(movie_data['rating']) for movie_data in movies_data.values()]
        length_movie_data = len(all_rating)
        average_rating = round(sum(all_rating) / length_movie_data, 2)
        all_rating.sort()
        if length_movie_data % 2 == 0:
            index = length_movie_data // 2
            median_rating = (all_rating[index] + all_rating[index - 1]) / 2
        else:
            index = length_movie_data // 2
            median_rating = all_rating[index]
        best_movie = max(movies_data.items(), key=lambda x: x[1]['rating'])
        worst_movie = min(movies_data.items(), key=lambda x: x[1]['rating'])
        print(f"Average rating: {average_rating}")
        print(f"Median rating: {median_rating}")
        print(f"Best movie: {best_movie[0]}, {best_movie[1]['rating']}")
        print(f"Worst movie: {worst_movie[0]}, {worst_movie[1]['rating']}")


    def _command_creating_histogram(self):
        """
        Creates a histogram based on the ratings of the movies obtained from the storage.

        Retrieves the movie data from the storage and extracts the ratings of the movies.
        Then, a histogram is generated using Matplotlib to visualize the distribution of movie ratings.
        The x-axis represents the movie ratings, the y-axis represents the number of movies within
        each rating range, and the histogram is divided into 10 bins.

        The user is prompted to enter a filename (e.g., ratings.png) to save the histogram as an image.
        Upon saving the histogram, a confirmation message is printed displaying the filename under which
        the histogram image was saved.

        Returns:
            None
        """
        movies_data = self._storage.list_movies()
        ratings = [movie['rating'] for movie in movies_data.values()]
        plt.hist(ratings, bins=10)
        plt.xlabel("Movie Rating")
        plt.ylabel("Number of Movies")
        plt.title("Distribution of Movie Ratings")
        plt.grid(True)
        filename = input("Enter filename (e.g., ratings.png): ")
        plt.savefig(filename)
        print(f"Histogram saved as {filename}")


    def generate_movie_page(self):
        """
        Generates individual HTML pages for each movie based
        on the movie data stored in the movie storage.
        
        Retrieves all movies data from the movie storage.
        Reads the movie HTML template from the specified path.
        Iterates through each movie, replaces placeholders
        in the HTML template with movie-specific data,
        and writes the new HTML page for each movie.
        Prints a success message after generating all movie pages.

        Returns:
        None
        """
        all_movies_data = self._storage.list_movies()
        movie_html_string = docs_parcer.read_html(MOVIE_HTML_PATH)
        for title, movie in all_movies_data.items():
            new_html_movie = movie_html_string.replace(
            '__MOVIE_NAME__', title
            )
            poster_string = f"<img class='movie-poster' src={movie['poster']}> \n"
            new_html_movie = new_html_movie.replace('__MOVIE_POSTER__', poster_string)
            description_string = ''
            description_string += f"<div class='movie-description'>"
            description_string += f"<ul><li>Director:{movie['director']}</li>"
            description_string += f"<li>Genre: {movie['genre']} </li> </ul> "
            description_string += f"Summary: {movie['plot']} </div>"
            description_string += f"<p><button><a href='index.html'>RETURN</a></button></p>"
            new_html_movie = new_html_movie.replace(
            '__MOVIE_DESCRIPTION__', description_string
            )
            docs_parcer.write_new_html(new_html_movie, f'_static/movie_{title}.html')
        print("Movie pages was successfully generated")


    def _generate_website(self):
        """
        Generate a web site based on the movie data.

        This function retrieves all movies data from the movie storage, 
        reads an HTML template, replaces
        the title with the output website name, 
        generates HTML content for each movie,
        replaces the movie grid template 
        in the HTML with the generated movie content,
        writes the new HTML data 
        to a file, and prints a success message.

        Returns:
        None
        """
        all_movies_data = self._storage.list_movies()
        html_string = docs_parcer.read_html(INDEX_HTML_PATH)
        output_website_name = 'Interesting movies - website for everyone'
        new_html_data = html_string.replace("__TEMPLATE_TITLE__", output_website_name)
        output_movies = ''
        for title, movie in all_movies_data.items():
            output_movies += '\n<li> <div class="movie"> '
            output_movies += f"<img class='movie-poster' src={movie['poster']}>"
            output_movies += f"<div class='movie-title'><a href='./movie_{title}"
            output_movies += f".html'>{title}</a></div>"
            output_movies += f"<div class='movie-year'>{movie['year_of_release']}</div>"
            output_movies += f"<div class='movie-rating'>"
            output_movies += f"<span class='rating-value'>{movie['rating']}</span></div>"
            if 'notes' in movie:
                output_movies += f"<div class='movie-note'>{movie['notes']}</div>"
            output_movies += '</div> \n </li>'
        new_html_data = new_html_data.replace('__TEMPLATE_MOVIE_GRID__', output_movies)
        self.generate_movie_page()
        docs_parcer.write_new_html(new_html_data, '_static/index.html')
        print('Website was generated successfully.')


    @staticmethod
    def exit_program():
        """
        Exit the program.

        Returns:
        None
        """
        print()
        print("\nBye!\n")
        sys.exit() # noqa: E0602


    @staticmethod
    def get_user_input():
        """
        Get user input for menu options and validate the input.

        Returns:
        int: User's choice for the menu option.
        """
        while True:
            user_input = input("Enter choice (0-10): ")
            try:
                user_input = int(user_input)
                if 0 <= user_input <= 10:
                    return user_input
                else:
                    print("Invalid input. Please enter a number between 0 and 10.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")


    @staticmethod
    def display_menu():
        """
        Display the menu options for the program.

        Returns:
        None
        """
        print("********** My Movies Database **********")
        print("Menu:\n0. Exit\n1. List movies\n2. Add movie\n3."
            " Delete movie\n4. Update movie\n5. Stats\n6."
            " Random movie\n7. Search movie\n8."
            " Movies sorted by rating\n9."
            " Create Rating Histogram\n10. Generate website\n")


    def run(self):
        """
        Main function to run the program and interact with the user.

        Returns:
        None
        """
        self.display_menu()

        while True:
            user_input = self.get_user_input()
            menu_functionality = {
                0: self.exit_program,
                1: self._command_list_movies,
                2: self._command_add_movie,
                3: self._command_delete_movie,
                4: self._command_update_movie,
                5: self._command_movie_stats,
                6: self._command_random_movie,
                7: self._command_search,
                8: self._command_sorted_movies,
                9: self._command_creating_histogram,
                10: self._generate_website
        }
            if user_input in menu_functionality:
                menu_functionality[user_input]()
            else:
                print("You entered the wrong key")
            choice = input("\nPress Enter to continue\n")
            self.display_menu()
            if choice != '':
                break



storage2 = StorageCsv("mom.csv")
movies = MovieApp(storage2)
movies._command_movie_stats()