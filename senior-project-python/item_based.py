from imports import *


def manhattan_distance(a: list, b: list):
    """
    takes in two lists and returns manhattan distance
    """
    return sum((abs(e1 - e2)) for e1, e2 in zip(a, b))


def euclidean_distance(a: list, b: list):
    """
    takes in two lists and returns euclidean distance
    """
    return sqrt(sum((e1 - e2) ** 2 for e1, e2 in zip(a, b)))


def get_feature_list(a):
    """
    returns the list of features for a specific song (excluding song id, name, artists, etc.)
    """
    if len(list(a.values())):
        a = list(a.values())[4:10]
    else:
        a = list(a.values())[4:-2]
    return [float(x) for x in a]


def kNN(song_index, data, k, distance_metric='euclidean'):
    """
  k-Nearest-Neighbors algorithm implementation,
  song_index : int -> index of song we are getting similarity for
  data_list : list -> data to index song from
  k : int -> number of nearest neighbors to return according to similarity metric
  """
    tmp = data.copy()
    a = get_feature_list(tmp[song_index])
    for x in range(0, len(tmp)):
        b = get_feature_list(tmp[x])
        if distance_metric == 'euclidean':
            tmp[x]['distance'] = euclidean_distance(a, b)
        else:
            tmp[x]['distance'] = manhattan_distance(a, b)
    tmp = sorted(tmp, key=lambda d: d['distance'])
    result = []
    for x in range(1, k + 1):
        result.append(tmp[x])
    return result


def get_recommendations(result):
    """
    The result is k dictionaries containing information about the recommended songs
    this function returns their ids and their similarity scores to be appended to the json file
    """
    recommendations = []
    sim_scores = []
    for song in result:
        recommendations.append(song['id'])
        distance = str(int((1 - song['distance']) * 100))
        sim_scores.append(distance)
    for i in range(5):
        sim_scores.append('-')
    return recommendations, sim_scores
