from user_based import *
from item_based import *


def hybrid_filtering(data, user_song_ratings):
    """
    Combines recommendations from both the item-based and user-based recommender systems
    saves the output to a json file to be sent to the front-end
    """
    user_rec = kNN_users(user_index, user_song_ratings, k, data, index, 'euclidean')
    item_rec = kNN(index, data, k, 'euclidean')

    recommendations, sim_scores = get_recommendations(item_rec)
    for x in list(user_rec.keys()):
        recommendations.append(x)
    append_recommendation_as_json(data[index], recommendations, sim_scores, 'item_based_recommendations')


def main():
    data = read_csv(big_data_PATH)
    user_song_ratings = read_csv(user_ratings_PATH)
    hybrid_filtering(data, user_song_ratings)


if __name__ == '__main__':
    main()
