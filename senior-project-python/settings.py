"""
Holds paths to datasets used and indices to song and user (for which we want to get a recommendation)
"""
big_data_PATH = 'assets/big_data.csv'
data_subset_genre_PATH = 'assets/data_subset_genre.csv'
user_ratings_PATH = 'assets/user_song_ratings.csv'
genres = ['Blues', 'Country', 'Easy listening', 'Electronic', 'Contemporary folk', 'Hip hop',
          'Jazz', 'Pop', 'R&B and soul', 'Rock', 'Metal', 'Punk']
index = 12011
user_index = 231
k = 5  # the k nearest neighbors to find
