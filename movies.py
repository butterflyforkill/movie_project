import random
import matplotlib.pyplot as plt


def list_of_movies(movies_dic):
    """
    Print the list of movies with their ratings and year of release.

    Args:
    movies_dic (dict): A dictionary containing movie names as keys and their corresponding rating and year of release as values.

    Returns:
    None
    """
    length = len(movies_dic)
    print(f"{length} movies in total")
    for movie_name, movies_data in movies_dic.items():
        print(f"{movie_name}: {movies_data['rating']}, {movies_data['year_of_release']}")


def add_movie(movies_dic):
    """
    Add a new movie to the movies dictionary.

    Args:
    movies_dic (dict): A dictionary containing movie names as keys and their corresponding rating and year of release as values.

    Returns:
    None
    """
    movie = input("Enter new movie name: ")
    rating = float(input("Enter new movie rating: "))
    year = int(input("Please, enter the year of release: "))
    movies_dic[movie] = {
        'rating': rating,
        'year_of_release': year
    }
    print(f"Movie {movie} successfully added")


def delete_movie(movies_dic):
    """
    Delete a movie from the movies dictionary.

    Args:
    movies_dic (dict): A dictionary containing movie names as keys and their corresponding rating and year of release as values.

    Returns:
    None
    """
    movie = input("Enter movie name to delete: ")
    if movie in movies_dic:
        del movies_dic[movie]
        print(f"Movie {movie} successfully deleted")
    else:
        print(f"ERROR: {movie} doesn't exist in the library")


def update_movie(movies_dic):
    """
    Update the rating of an existing movie in the movies dictionary.

    Args:
    movies_dic (dict): A dictionary containing movie names as keys and their corresponding rating and year of release as values.

    Returns:
    None
    """
    movie = input("Enter movie name: ")
    rating = float(input("Enter new movie rating: "))
    if movie in movies_dic:
        movies_dic[movie].update([('rating', rating)])
        print(f"Movie {movie} successfully updated")
    else:
        print(f"ERROR: {movie} doesn't exist in the library")


def stats(movies_dic):
    """
    Calculate and print statistics such as average rating, median rating, best movie, and worst movie from the movies dictionary.

    Args:
    movies_dic (dict): A dictionary containing movie names as keys and their corresponding rating and year of release as values.

    Returns:
    None
    """
    all_rating = [movie_data['rating'] for movie_data in movies_dic.values()]
    
    length_movie_dic = len(all_rating)
    
    average_rating = sum(all_rating) / length_movie_dic
    
    all_rating.sort()
    
    if length_movie_dic % 2 == 0:
        index = length_movie_dic // 2
        median_rating = (all_rating[index] + all_rating[index - 1]) / 2
    else:
        index = length_movie_dic // 2
        median_rating = all_rating[index]
    
    best_movie = max(movies_dic.items(), key=lambda x: x[1]['rating'])
    
    worst_movie = min(movies_dic.items(), key=lambda x: x[1]['rating'])
    
    print(f"Average rating: {average_rating}")
    print(f"Median rating: {median_rating}")
    print(f"Best movie: {best_movie[0]}, {best_movie[1]['rating']}")
    print(f"Worst movie: {worst_movie[0]}, {worst_movie[1]['rating']}")


def random_movie(movies_dic):
    """
    Select and print a random movie from the movies dictionary.

    Args:
    movies_dic (dict): A dictionary containing movie names as keys and their corresponding rating and year of release as values.

    Returns:
    None
    """
    [random_movie] = random.sample(sorted(movies_dic.items()), 1)
    print(f"Your movie for tonight: {random_movie[0]}, it's rated {random_movie[1]['rating']}")


def search_movie(movies_dic):
    """
    Search for a movie in the movies dictionary based on a partial movie name and print the matching results.

    Args:
    movies_dic (dict): A dictionary containing movie names as keys and their corresponding rating and year of release as values.

    Returns:
    None
    """
    search_path = input("Enter part of movie name: ")
    for movie, movie_data in movies_dic.items():
        if search_path.lower() in movie.lower():
            print(f"{movie}, {movie_data['rating']}")


def movies_sorted(movies_dic):
    """
    Sort and print the movies in the movies dictionary based on their ratings in descending order.

    Args:
    movies_dic (dict): A dictionary containing movie names as keys and their corresponding rating and year of release as values.

    Returns:
    None
    """
    sorted_movies = sorted(movies_dic.items(), key=lambda item: item[1]['rating'], reverse=True)
    for movie, details in sorted_movies:
        print(f"{movie}: {details['rating']}")


def create_rating_histogram(movies_dic):
    """
    Create a histogram of movie ratings and save it as an image file.

    Args:
    movies_dic (dict): A dictionary containing movie names as keys and their corresponding rating and year of release as values.

    Returns:
    None
    """
    ratings = [movie['rating'] for movie in movies_dic.values()]
    plt.hist(ratings, bins=10)
    plt.xlabel("Movie Rating")
    plt.ylabel("Number of Movies")
    plt.title("Distribution of Movie Ratings")
    plt.grid(True)
    filename = input("Enter filename (e.g., ratings.png): ")
    plt.savefig(filename)
    print(f"Histogram saved as {filename}")


def exit_program():
    """
    Exit the program.

    Returns:
    None
    """
    print("Bye!")
    exit()  # Terminate the program


def display_menu():
    """
    Display the menu options for the program.

    Returns:
    None
    """
    print("********** My Movies Database **********")
    print(f"Menu:\n0. Exit\n1. List movies\n2. Add movie\n3." 
          f" Delete movie\n4. Update movie\n5. Stats\n6."
          f" Random movie\n7. Search movie\n8. Movies sorted by rating\n9."
          f" Create Rating Histogram\n")

def get_user_input():
    """
    Get user input for menu options and validate the input.

    Returns:
    int: User's choice for the menu option.
    """
    while True:
        try:
            user_input = int(input("Enter choice (0-9): "))
            if 0 <= user_input <= 9:
                return user_input
            else:
                print("You entered the wrong key")
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    """
    Main function to run the program and interact with the user.

    Returns:
    None
    """
    # Dictionary to store the movies and the rating
    movies = {
        "The Shawshank Redemption": {
            'rating': 9.5,
            'year_of_release': 1964
            },
        "Pulp Fiction": {
            'rating': 9.5, 
            'year_of_release': 1964
            },
        "The Room": {
            'rating': 9.5, 
            'year_of_release': 1964
            },
        "The Godfather": {
            'rating': 9.5, 
            'year_of_release': 1964
            },
        "The Godfather: Part II": {
            'rating': 9.5, 
            'year_of_release': 1964
            },
        "The Dark Knight": {
            'rating': 9.5, 
            'year_of_release': 1964}
            ,
        "12 Angry Men": {
            'rating': 1.9, 
            'year_of_release': 1964
            },
        "Everything Everywhere All At Once": {
            'rating': 9.5,
             'year_of_release': 1964
             },
        "Forrest Gump": {
            'rating': 9.5, 
            'year_of_release': 1964
            },
        "Star Wars: Episode V": {
            'rating': 9.5, 
            'year_of_release': 1964
            }
    }       

    # Your code here
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
            9: create_rating_histogram
       }
        if user_input == 0:
            menu_functionality[user_input]()
        elif user_input in menu_functionality:
            menu_functionality[user_input](movies)
        else:
            print("You entered the wrong key")
        choice = input("Press Enter to continue")
        if choice != '':
            break
        else:
            display_menu()


if __name__ == "__main__":
    main()
