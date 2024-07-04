import random
import sys
import matplotlib.pyplot as plt
import requests
import movie_storage
import html_parcer
from config.config_files import APIkeys

INDEX_HTML_PATH = '_static/index_template.html'
MOVIE_HTML_PATH = '_static/movie_template.html'


def list_of_movies():
    """
    Print the list of movies with their ratings and year of release.

    Args:
    movies_dic (dict): A dictionary containing movie names
      as keys and their corresponding rating and
      year of release as values.

    Returns:
    None
    """
    movies_data = movie_storage.get_movies()
    length = len(movies_data)
    print(f"\n{length} movies in total\n")
    for movie_name, movie_data in movies_data.items():
        print(f"{movie_name}: {movie_data['rating']}, {movie_data['year_of_release']}")


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


def add_movie():
    """
    Add a new movie to the movies dictionary.

    Args:
    movies_dic (dict): A dictionary containing movie names
      as keys and their corresponding rating and year of release as values.

    Returns:
    None
    """
    movie = input("Enter new movie name: ")
    all_movies = movie_storage.get_movies()
    if movie in all_movies:
        print(f"Movie {movie} already exist!")
        return
    api_url = f'http://www.omdbapi.com/?apikey={APIkeys.APIkey}&t={movie}'
    response = requests.get(api_url)
    parsed_resp = response_parser(response)
    if parsed_resp == 'Error: Movie not found!':
        print(f"The movie {movie} doesn't exist")
    elif type(parsed_resp) == str:
        print(parsed_resp)
    else:
        rating = float(parsed_resp['Ratings'][0]['Value'].split('/')[0])
        year_str = parsed_resp['Year'] 
        year = year_str[0:4]
        print(rating)
        movie_storage.add_movie(
            movie,
            year, 
            rating, 
            parsed_resp['Poster'],
            parsed_resp['Plot'],
            parsed_resp['Genre'],
            parsed_resp['Director']
            )
        print(f"Movie {movie} successfully added")


def delete_movie():
    """
    Delete a movie from the movies dictionary.

    Args:
    movies_dic (dict): A dictionary containing movie names
      as keys and their corresponding rating and year of release as values.

    Returns:
    None
    """
    movie = input("Enter movie name to delete: ")
    movie_storage.delete_movie(movie)


def update_movie():
    """
    Update the rating of an existing movie in the movies dictionary.

    Args:
    movies_dic (dict): A dictionary containing movie names
      as keys and their corresponding rating and year of release as values.

    Returns:
    None
    """
    movie = input("Enter movie name: ")
    notes = input("Enter movie notes: ")
    movie_storage.update_movie(movie, notes)


def stats():
    """
    Calculate and print statistics such as average rating,
    median rating, best movie, and worst movie from the movies dictionary.

    Args:
    movies_dic (dict): A dictionary containing movie names
      as keys and their corresponding rating and year of release as values.

    Returns:
    None
    """
    movies_data = movie_storage.get_movies()
    all_rating = [movie_data['rating'] for movie_data in movies_data.values()]
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


def random_movie():
    """
    Select and print a random movie from the movies dictionary.

    Args:
    movies_dic (dict): A dictionary containing movie names
      as keys and their corresponding rating and year of release as values.

    Returns:
    None
    """
    movies_data = movie_storage.get_movies()
    [random_movie_dict] = random.sample(sorted(movies_data.items()), 1)
    print(f"Your movie for tonight: {random_movie_dict[0]},"
          f"it's rated {random_movie_dict[1]['rating']}")


def search_movie():
    """
    Search for a movie in the movies dictionary based
    on a partial movie name and print the matching results.

    Args:
    movies_dic (dict): A dictionary containing movie names
      as keys and their corresponding rating and year of release as values.

    Returns:
    None
    """
    movies_data = movie_storage.get_movies()
    search_path = input("Enter part of movie name: ")
    for movie, movie_data in movies_data.items():
        if search_path.lower() in movie.lower():
            print(f"{movie}, {movie_data['rating']}")


def movies_sorted():
    """
    Sort and print the movies in the movies dictionary based
    on their ratings in descending order.

    Args:
    movies_dic (dict): A dictionary containing movie names
      as keys and their corresponding rating and year of release as values.

    Returns:
    None
    """
    movies_data = movie_storage.get_movies()
    sorted_movies = sorted(movies_data.items(), key=lambda item: item[1]['rating'], reverse=True)
    for movie, details in sorted_movies:
        print(f"{movie}: {details['rating']}")


def create_rating_histogram():
    """
    Create a histogram of movie ratings and save it as an image file.

    Args:
    movies_dic (dict): A dictionary containing movie names
      as keys and their corresponding rating and year of release as values.

    Returns:
    None
    """
    movies_data = movie_storage.get_movies()
    ratings = [movie['rating'] for movie in movies_data.values()]
    plt.hist(ratings, bins=10)
    plt.xlabel("Movie Rating")
    plt.ylabel("Number of Movies")
    plt.title("Distribution of Movie Ratings")
    plt.grid(True)
    filename = input("Enter filename (e.g., ratings.png): ")
    plt.savefig(filename)
    print(f"Histogram saved as {filename}")


def generate_movie_page():
    all_movies_data = movie_storage.get_movies()
    movie_html_string = html_parcer.read_html(MOVIE_HTML_PATH)
    for title, movie in all_movies_data.items():
        new_html_movie = movie_html_string.replace('__MOVIE_NAME__', title)
        poster_string = f"<img class='movie-poster' src={movie['poster']}> \n"
        new_html_movie = new_html_movie.replace('__MOVIE_POSTER__', poster_string)
        description_string = ''
        description_string += f"<div class='movie-description'> <ul><li>Director: {movie['director']} </li>"
        description_string += f"<li>Genre: {movie['genre']} </li> </ul> "
        description_string += f"Summary: {movie['plot']} </div> <p><button><a href='index.html'>RETURN</a></button></p>"
        new_html_movie = new_html_movie.replace('__MOVIE_DESCRIPTION__', description_string)
        html_parcer.write_new_html(new_html_movie, f'_static/movie_{title}.html')
    print("Movie page was successfully generated")
    
        
def generate_web_site():
    """
    Generate a web site based on the movie data.

    This function retrieves all movies data from the movie storage, 
    reads an HTML template, replaces the title with the output website name, 
    generates HTML content for each movie, replaces the movie grid template 
    in the HTML with the generated movie content, writes the new HTML data 
    to a file, and prints a success message.

    Returns:
    None
    """
    all_movies_data = movie_storage.get_movies()
    html_string = html_parcer.read_html(INDEX_HTML_PATH)
    output_website_name = 'Interesting movies - website for everyone'
    new_html_data = html_string.replace("__TEMPLATE_TITLE__", output_website_name)
    output_movies = ''
    for title, movie in all_movies_data.items():
        output_movies += '\n<li> <div class="movie"> '
        output_movies += f"<img class='movie-poster' src={movie['poster']}> \n"
        output_movies += f"<div class='movie-title'><a href='./movie_{title}.html'>{title}</a></div> \n"
        output_movies += f"<div class='movie-year'>{movie['year_of_release']}</div> \n"
        output_movies += f"<div class='movie-rating'>"
        output_movies += f"<span class='rating-value'>{movie['rating']}</span></div>"
        if 'notes' in movie:
            output_movies += f"<div class='movie-note'>{movie['notes']}</div>"
        output_movies += '</div> \n </li>'
    new_html_data = new_html_data.replace('__TEMPLATE_MOVIE_GRID__', output_movies)
    generate_movie_page()
    html_parcer.write_new_html(new_html_data, '_static/index.html')
    print('Website was generated successfully.')


def exit_program():
    """
    Exit the program.

    Returns:
    None
    """
    print()
    print("\nBye!\n")
    sys.exit() # noqa: E0602


def display_menu():
    """
    Display the menu options for the program.

    Returns:
    None
    """
    print("********** My Movies Database **********")
    print("Menu:\n0. Exit\n1. List movies\n2. Add movie\n3."
          " Delete movie\n4. Update movie\n5. Stats\n6."
          " Random movie\n7. Search movie\n8. Movies sorted by rating\n9."
          " Create Rating Histogram\n10. Generate website\n")

def get_user_input():
    """
    Get user input for menu options and validate the input.

    Returns:
    int: User's choice for the menu option.
    """
    while True:
        try:
            user_input = int(input("Enter choice (0-10): "))
            if 0 <= user_input <= 10:
                return user_input
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    """
    Main function to run the program and interact with the user.

    Returns:
    None
    """
    display_menu()

    while True:
        user_input = get_user_input()
        menu_functionality = {
            0: exit_program,
            1: list_of_movies,
            2: add_movie,
            3: delete_movie,
            4: update_movie,
            5: stats,
            6: random_movie,
            7: search_movie,
            8: movies_sorted,
            9: create_rating_histogram,
            10: generate_web_site
       }
        if user_input in menu_functionality:
            menu_functionality[user_input]()
        else:
            print("You entered the wrong key")
        choice = input("\nPress Enter to continue\n")
        display_menu()
        if choice != '':
            break


if __name__ == "__main__":
    main()
