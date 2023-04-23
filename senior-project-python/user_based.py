from data_cleaning_preparation import *

"""
GENERATING USERS
"""


class User:
    """
    A user has an ID, a list of genre preferences and a {song : rating} dictionary
    """
    _user_ids = []

    def generate_userID(self):
        characters = string.ascii_letters + string.digits
        user_id = ''.join(random.choice(characters) for i in range(10))
        if user_id not in self._user_ids:
            self._user_ids.append(user_id)
            return user_id
        else:
            return self.generate_userID()

    def __init__(self, genre_preferences, song_ratings: dict):
        self.user_id = self.generate_userID()
        self.genre_preferences = genre_preferences
        self.song_ratings = song_ratings

    def get_user_id(self):
        return self.user_id

    def get_genre_preferences(self):
        return self.genre_preferences

    def set_genre_preferences(self, new_genre_preferences):
        self.genre_preferences = new_genre_preferences

    def get_song_ratings(self):
        return self.song_ratings

    def set_song_ratings(self, new_song_ratings):
        self.song_ratings = new_song_ratings


def get_music_preferences(genres: list):
    """
    returns 6 random genre preferences for a user
    facilitates the creation of users
    """
    # each user has 6/12 genre preferences
    return random.sample(genres, 6)


def rate_song(song, genre_preferences):
    """
    gives a rating on a song based on whether the song's genre is in the user's preferences or not
    """
    if song['genre'] in genre_preferences:
        return random.randint(6, 10)
    else:
        return random.randint(1, 5)


def get_song_ratings(data, n, genre_preferences):
    """
  Returns a dictionary of random (song:rating) pairs
  data contains all the songs with all their features
  n determines how many records that dictionary will contain
  genre_preferences is a list of the genres that this user likes
  """
    result = {}
    songs = random.sample(data, n)
    for song in songs:
        result[song['id']] = rate_song(song, genre_preferences)
    return result


def generate_users(data, n, m):
    """
  Generate a number (n) of users with random genre preferences
  and random songs they've listened to along with their ratings
  Each user has an m number of song_ratings
  """
    # hold all users in a list
    users = []
    for i in range(n):
        random_preferences = get_music_preferences(genres)
        song_ratings = get_song_ratings(data, m, random_preferences)
        users.append(User(random_preferences, song_ratings))
    return users


def create_user_rating_matrix(users, data):
    """
    Creates a list of dictionaries with each row being a user
    each user has an index, user ID, and {songID : rating} pairs
    """
    user_ratings = []
    songs = [song['id'] for song in data]
    i = 0
    for user in users:
        row = {'index': i, 'user_id': user.get_user_id()}
        song_ratings = user.get_song_ratings()
        for song in songs:
            if song in song_ratings.keys():
                row[song] = song_ratings[song]
            else:
                row[song] = 0
        user_ratings.append(row)
        i += 1
    return user_ratings


"""
USER BASED KNN
"""


def id_to_genre(data):
    """
    returns a dictionary of {songID : genre} pairs
    """
    id_genre = {}
    for x in data:
        id_genre[x['id']] = x['genre']
    return id_genre


def find_user_pref(data, id_genre, user_id):
    """
    A user will rate songs 6-10 from the genres he likes
    the function finds the genres of songs with rating > 6 and returns when it finds the 6 genres the user likes
    """

    genre_pref = []
    i = 0
    for key, value in data[user_id].items():
        if i < 2:
            i += 1
            continue
        if int(value) >= 6:
            if id_genre[key] not in genre_pref:
                genre_pref.append(id_genre[key])
    return genre_pref


def reset_indices_user(data):
    """
    resets the indices for the user song ratings matrix
    """
    for i in range(len(data)):
        data[i]['index'] = i
    return data


def find_intersection(a, b):
    """
    returns the songs that both users have rated (songs that are not rated have a rating of 0)
    """
    c = []
    d = []
    for i in range(len(a)):
        if a[i] != 0 and b[i] != 0:
            c.append(a[i])
            d.append(b[i])
    return c, d


def get_user_ratings(a):
    """
    returns the ratings of songs of user a
    """
    songs = list(a.values())[2:]
    num_songs = 6416
    if len(songs) == num_songs:
        songs = songs[:-1]
    return [x for x in songs]


def manhattan_distance_users(a: list, b: list):
    """
    takes in two lists and returns manhattan distance
    """
    c, d = find_intersection(a, b)
    return sum((abs(e1 - e2)) for e1, e2 in zip(c, d))


def euclidean_distance_users(a: list, b: list):
    """
  takes in two lists and returns euclidean distance
  """
    c, d = find_intersection(a, b)
    return sqrt(sum((e1 - e2) ** 2 for e1, e2 in zip(c, d)))


def normalize_distances(a):
    """
    normalizes distances (0-1)
    """
    norm = [(float(i) - min(a)) / (max(a) - min(a)) for i in a]
    return norm


def filter_unrated_songs(user):
    """
    returns the songs that the user has not listened to
    """
    possible_rec = []
    for key, value in list(user.items())[2:]:
        if key == 'distance':
            continue
        if int(value) == 0:
            possible_rec.append(key)
    return possible_rec


def get_user_song_recommendations(data, index, similar_users, songs, song_index):
    """
    Takes a list of similar users to the active user who is at given index
    Returns five songs as recommendations from the songs that the active user has not listened to
    """
    user = data[index]
    artist = get_first_artist(songs, song_index)
    genre = get_scraped_genre(artist)
    gen_genres = get_general_genres()
    songs[song_index]['genre'] = genre
    result = generalize_genres([songs[song_index]], gen_genres)

    if result:
        songs[song_index] = result[0]
        genre = songs[song_index]['genre']
    else:
        genre = None
    # id_genre will know the genres of all the songs in the subset from which the users are created
    id_genre = {}
    subset = read_csv(data_subset_genre_PATH)
    for x in subset:
        id_genre[x['id']] = x['genre']
    unrated_songs = filter_unrated_songs(user)
    # song_ratings will hold (song_id : predicted_rating) entries and recommend the ones with highest predicted rating
    song_ratings = {}
    for song_id in unrated_songs:
        nominator = 0
        denominator = 0
        for x in similar_users:
            if int(x[song_id]) != 0:
                sim_score = round(1 - x['distance'], 2)
                nominator += float(x[song_id]) * float(sim_score)
                denominator += float(sim_score)
        if denominator != 0:
            predicted_rating = round((nominator / denominator), 2)
        else:
            continue
        song_ratings[song_id] = predicted_rating
    top_5_keys = sorted(song_ratings, key=song_ratings.get, reverse=True)
    top_5_songs = []
    if genre:
        for x in top_5_keys:
            if id_genre[x] == genre:
                top_5_songs.append(x)
            if len(top_5_songs) == 5:
                break
    else:
        top_5_songs = top_5_keys[0:5]
    result = {}
    for x in top_5_songs:
        result[x] = str(song_ratings[x]) + ' ' + id_genre[x]
    return result


def kNN_users(user_index, data, k, songs, song_index, distance_metric='euclidean'):
    """
  k-Nearest-Neighbors algoirthm implementation,
  song_index : int -> index of song we are getting similarity for
  data_list : list -> data to index song from
  k : int -> number of nearest neighbors to return according to similarity metric
  """
    tmp = data.copy()
    a = get_user_ratings(tmp[user_index])
    a = list(map(int, a))
    for x in range(0, len(tmp)):
        b = get_user_ratings(tmp[x])
        b = list(map(int, b))
        if distance_metric == 'euclidean':
            tmp[x]['distance'] = euclidean_distance_users(a, b)
        else:
            tmp[x]['distance'] = manhattan_distance_users(a, b)
    tmp = sorted(tmp, key=lambda d: d['distance'])
    result = []
    distances = [x['distance'] for x in tmp]
    normalized_distances = normalize_distances(distances)
    for i in range(len(tmp)):
        tmp[i]['distance'] = round(normalized_distances[i], 2)
    for x in range(1, k + 1):
        result.append(tmp[x])
    return get_user_song_recommendations(data, user_index, result, songs, song_index)
