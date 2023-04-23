from data_cleaning_preparation import *
from item_based import *
from user_based import *
from settings import *
import unittest
import sys

sys.path.insert(0, '..')


class TestMusicRecommender(unittest.TestCase):

    def setUp(self) -> None:
        self.data = read_csv('../' + big_data_PATH)
        self.user_data = read_csv('../' + user_ratings_PATH)
        self.s1 = {'': 0, 'id': '5jx8tCxiO0uIbo2uNia23K',
                   'name': '$S*ummertime? S@adness', 'artists': '[\'Lana Del Rey\']'}
        self.s2 = {'': 1, 'id': '5jx8tCxiO0uIbo2uNia23K',
                   'name': 'Summertime Sadness', 'artists': '[\'Lana Del Rey\']'}
        self.s3 = {'': 2, 'id': '0d0jsoba88SpOoFxCxA2rZ',
                   'name': 'The Art of Peer Pressure', 'artists': '[\'Kendrick Lamar\']'}
        self.example_data = [self.s1, self.s2, self.s3]
        self.a = [1, 2, 3, 4]
        self.b = [5, 6, 7, 8]
        self.ratings_a = [10, 0, 2, 6, 0, 5]
        self.ratings_b = [0, 7, 4, 0, 1, 8]

    def test_reset_indices(self):
        self.data = reset_indices(self.data)
        self.assertEqual(576, self.data[576][''])

    def test_get_first_artist(self):
        i = 114618
        self.assertEqual('The_Weeknd', get_first_artist(self.data, i))

    def test_remove_special_chars(self):
        self.assertEqual(2, len(remove_special_chars(self.example_data)))

    def test_find_duplicates(self):
        self.assertEqual([1], find_duplicates(self.example_data))

    def test_delete_duplicates(self):
        result = delete_duplicates(self.example_data, [1])
        self.assertEqual(2, len(result))

    def test_get_unique_artists(self):
        self.assertEqual(2, len(get_unique_artists(self.example_data)))

    def test_euclidean_distance(self):
        self.assertEqual(8, euclidean_distance(self.a, self.b))

    def test_manhattan_distance(self):
        self.assertEqual(16, manhattan_distance(self.a, self.b))

    def test_get_feature_list(self):
        feature_list = [0.658, 0.713, 0.44, 2.24e-05, 0.809, -4.714]
        self.assertEqual(feature_list, get_feature_list(self.data[313]))

    def test_find_intersection(self):
        self.assertEqual(([2, 5], [4, 8]), find_intersection(
            self.ratings_a, self.ratings_b))

    def test_manhattan_distance_users(self):
        self.assertEqual(5, manhattan_distance_users(
            self.ratings_a, self.ratings_b))
