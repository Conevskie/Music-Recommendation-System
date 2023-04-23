"""
DATA CLEANING AND SCRAPING GENRES
"""

from reading_writing import *
from user_based import *


def find_duplicates(data):
    """
    returns a list of indices of the duplicates found in the data (by id)
    """
    song_names = []
    duplicate_indices = []
    for i in range(len(data)):
        if data[i]['id'] in song_names:
            duplicate_indices.append(i)
        else:
            song_names.append(data[i]['id'])
    return duplicate_indices


def delete_duplicates(data, duplicates):
    """
    removes duplicates according to the duplicates list passed (obtained by find_duplicates())
    """
    for i in reversed(duplicates):
        del data[i]
    return data


def reset_indices(data):
    """
    resets indices of data, setting index = row number
    """
    for i in range(len(data)):
        data[i][''] = i
    return data


def remove_special_chars(data):
    """
    removes songs with special characters in their names
    """
    for i in range(len(data) - 1, -1, -1):
        if re.search(r'[!@#$%^&*]', data[i]['name']):
            del (data[i])
    return data


def add_year(data, cleaned_data, index):
    """
    adds year to the cleaned data
    """
    for i in range(len(cleaned_data)):
        for j in range(len(data)):
            if data[j]['id'] == data[i]['id']:
                index = j
        cleaned_data[i]['year'] = data[index]['year']
    return cleaned_data


def delete_year(data):
    """
    deletes year from old data
    """
    for x in range(len(data)):
        if len(data[x].values()) == 11:
            del data[x]['year']
    return data


def get_random_subset(data, size):
    """
    gets a random subset from the data (given size)
    """
    new_data = random.sample(data, size)
    return new_data


def get_unique_artists(data):
    """
    returns a list of all artists in data (unique)
    """
    artists = []
    for x in data:
        artists_str = x['artists']
        end = artists_str.find("'", 2)
        artist = artists_str[2:end]
        artist = artist.replace(" ", "_")
        if artist not in artists:
            artists.append(artist)
    return artists


def get_scraped_genre(artist):
    """
    given artists, returns genre of artist
    """
    url = 'https://en.wikipedia.org/wiki/' + artist
    print(url)

    page = requests.get(url)
    soup = bs(page.content, 'html.parser')
    s = soup.find_all('table', class_='infobox biography vcard')

    if len(s) == 0:
        s = soup.find_all('table', class_='infobox vcard plainlist')

    row = str(s)

    if row.find("Genres") != -1:
        genre_row_index = row.find("Genres", 10)
        title_genre_row_index = row.find("title=", genre_row_index)
        title_genre_row_index += 7
        genre = row[title_genre_row_index:row.find("\"", title_genre_row_index)]
    else:
        genre = ''

    return genre


def get_first_artist(data, index):
    """
    songs can have multiple artists saved in the data as ['artist1', 'artist2']
    this function returns the first artist - artist1
    """
    artists = data[index]['artists']
    end = artists.find("'", 2)
    artist = artists[2:end]
    artist = artist.replace(" ", "_")
    return artist


def get_genres(artists):
    """
    given a list of artists, it gets genre for each artist and returns list of genres
    """
    genres = {}
    num = len(artists)
    print(f'Fetching genre for {num} artists...')
    i = 0
    for artist in artists:
        print(i)
        i += 1
        genres[artist] = get_scraped_genre(artist)
    return genres


def set_genres(data, artist_genre: dict):
    """
    sets genres to each song in data according to its artist's genre
    """
    for i in range(len(data)):
        artist = get_first_artist(data, i)
        data[i]['genre'] = artist_genre[artist]


def get_general_genres():
    """
    returns a dictionary of {general_genre : subgenre} pairs
    """
    url = 'https://en.wikipedia.org/wiki/List_of_music_genres_and_styles'
    general_genres = []
    result = {}

    page = requests.get(url)
    soup = bs(page.content, 'html.parser')
    genres = soup.find_all('span', class_='mw-headline')
    sub_genres = soup.find_all(class_='div-col')

    g = list(genres)
    for x in g[3:15]:
        general_genres.append(x.get_text())

    s = list(sub_genres)
    i = 0
    for elem in s[:-5]:
        l = []
        a = s[i].find_all('a')
        for tag in a:
            l.append(tag.get_text())
        result[general_genres[i]] = l
        i += 1
        if i == 11:
            break
    return result


def generalize_genres(data, general_genres):
    """
    goes through genres in data and generalizes them
    """
    for i in range(len(data) - 1, -1, -1):
        flag = False
        for key, value in general_genres.items():
            if data[i]['genre'] in value:
                data[i]['genre'] = key
                flag = True
                break
        if not flag:
            del data[i]
    return data


def subset_general_genres(data):
    """
    this function creates a subset from the data and finds genres for it
    """
    subset = get_random_subset(data, 30000)
    unique_artists = get_unique_artists(subset)
    genres = get_genres(unique_artists)
    save_artists_genres_csv(genres, 'artist_genre')
    set_genres(subset, genres)
    write_to_csv(subset, 'new_subset')


def clean_item_based_data(data):
    """
    A function that takes in the original data and transforms it to data on which the KNN algorithm will work
    """
    dup_indices = find_duplicates(data)
    data = delete_duplicates(data, dup_indices)
    data = remove_special_chars(data)
    data = reset_indices(data)
    return data


def get_user_based_data(data):
    subset = subset_general_genres(data)
    users = generate_users(subset, 10000, 1000)
    user_rating_matrix = create_user_rating_matrix(users, subset)
    return user_rating_matrix

