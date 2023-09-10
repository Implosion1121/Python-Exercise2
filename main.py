import sqlite3

# Read the file and copy the content to a list
with open('stephen_king_adaptations.txt', 'r') as file:
    stephen_king_adaptations_list = [line.strip().split(',') for line in file]

# Establish a connection with the SQLite database
conn = sqlite3.connect('stephen_king_adaptations.db')
cursor = conn.cursor()

# Create the table
cursor.execute('''CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table (
                    movieID TEXT,
                    movieName TEXT,
                    movieYear INTEGER,
                    imdbRating REAL
                )''')

# Insert the content into the table
cursor.executemany('INSERT INTO stephen_king_adaptations_table VALUES (?, ?, ?, ?)',
                   stephen_king_adaptations_list)

# Commit the changes
conn.commit()

# Function to search for movies based on user input
def search_movies():
    while True:
        print("Please select an option:")
        print("1. Search by movie name")
        print("2. Search by movie year")
        print("3. Search by movie rating")
        print("4. STOP")
        choice = input("Enter your choice: ")

        if choice == '1':
            movie_name = input("Enter the movie name: ")
            cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieName = ?", (movie_name,))
            result = cursor.fetchone()

            if result:
                print("Movie found:")
                print("Movie ID:", result[0])
                print("Movie Name:", result[1])
                print("Movie Year:", result[2])
                print("IMDB Rating:", result[3])
            else:
                print("No such movie exists in our database")

        elif choice == '2':
            movie_year = int(input("Enter the movie year: "))
            cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieYear = ?", (movie_year,))
            results = cursor.fetchall()

            if results:
                print("Movies found for the year", movie_year)
                for result in results:
                    print("Movie ID:", result[0])
                    print("Movie Name:", result[1])
                    print("Movie Year:", result[2])
                    print("IMDB Rating:", result[3])
            else:
                print("No movies were found for that year in our database")

        elif choice == '3':
            rating = float(input("Enter the minimum rating: "))
            cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE imdbRating >= ?", (rating,))
            results = cursor.fetchall()

            if results:
                print("Movies with rating", rating, "and above:")
                for result in results:
                    print("Movie ID:", result[0])
                    print("Movie Name:", result[1])
                    print("Movie Year:", result[2])
                    print("IMDB Rating:", result[3])
            else:
                print("No movies at or above that rating were found in the database")

        elif choice == '4':
            break

        else:
            print("Invalid choice. Please try again.")

# Call the search_movies function
search_movies()

# Close the connection
conn.close()
