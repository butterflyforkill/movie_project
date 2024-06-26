import random
import matplotlib.pyplot as plt


def list_of_movies(movies_dic):
    length = len(movies_dic)
    print(f"{length} movies in total")
    for movie_name, movies_data in movies_dic.items():
        print(f"{movie_name}: {movies_data['rating']}, {movies_data['year_of_release']}")


def add_movie(movies_dic):
    movie = input("Enter new movie name: ")
    rating = float(input("Enter new movie rating: "))
    year = int(input("Please, enter the year of release: "))
    movies_dic[movie] = {
        'rating': rating,
        'year_of_release': year
    }
    print(f"Movie {movie} successfully added")


def delete_movie(movies_dic):
    movie = input("Enter movie name to delete: ")
    if movie in movies_dic:
        del movies_dic[movie]
        print(f"Movie {movie} successfully deleted")
    else:
        print(f"ERROR: {movie} doesn't exist in the library")


def update_movie(movies_dic):
    movie = input("Enter movie name: ")
    rating = float(input("Enter new movie rating: "))
    if movie in movies_dic:
        movies_dic[movie].update([('rating', rating)])
        print(f"Movie {movie} successfully updated")
    else:
        print(f"ERROR: {movie} doesn't exist in the library")


def stats(movies_dic):
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
    [random_movie] = random.sample(sorted(movies_dic.items()), 1)
    print(f"Your movie for tonight: {random_movie[0]}, it's rated {random_movie[1]['rating']}")


def search_movie(movies_dic):
    search_path = input("Enter part of movie name: ")
    for movie, movie_data in movies_dic.items():
        if search_path.lower() in movie.lower():
            print(f"{movie}, {movie_data['rating']}")


def movies_sorted(movies_dic):
    sorted_movies = sorted(movies_dic.items(), key=lambda item: item[1]['rating'], reverse=True)
    for movie, details in sorted_movies:
        print(f"{movie}: {details['rating']}")


def create_rating_histogram(movies_dic):
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
    """Exits the program."""
    print("Bye!")
    exit()  # Terminate the program


def display_menu():
    print("********** My Movies Database **********")
    print(f"Menu:\n0. Exit\n1. List movies\n2. Add movie\n3." 
          f" Delete movie\n4. Update movie\n5. Stats\n6."
          f" Random movie\n7. Search movie\n8. Movies sorted by rating\n9."
          f" Create Rating Histogram\n")

def get_user_input():
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
