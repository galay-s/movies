"""
Tests of data_tools.py
"""

import os
import json
import unittest
from collections import OrderedDict
from unittest.mock import patch

from app import app
from app.data_tools import FilmsPeopleCollector


class APITestCase(unittest.TestCase):
    """Class for api testing."""

    def test_movies_api(self):
        """Tests a good url."""
        tester = app.test_client(self)
        response = tester.get('/movies/', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'ALL MOVIES' in response.data)

    def test_bad_api(self):
        """Tests a bad url."""
        tester = app.test_client(self)
        response = tester.get('/bad_api/', content_type='html/text')
        self.assertEqual(response.status_code, 404)
        self.assertTrue(b'Not Found' in response.data)


class FilmsPeopleCollectorTestCase(unittest.TestCase):
    """Class for FilmsPeopleCollector class testing."""

    def setUp(self):
        self.collector = FilmsPeopleCollector()
        with open(self.get_file_path('input__relation_films_people.json'), 'r') as file_point:
            self.people_data = json.load(file_point, object_pairs_hook=OrderedDict)

    @staticmethod
    def get_file_path(file_name):
        """Return absolute file path."""
        return os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'fixtures',
            file_name,
        )

    def test__get_film_id(self):
        """Test of FilmsPeopleCollector.__get_film_id method."""
        film_id = '2baf70d1-42bb-4437-b551-e5fed5a87abe'
        film_url = 'https://ghibliapi.herokuapp.com/films/{}'.format(film_id)
        self.assertEqual(film_id, self.collector.__get_film_id(film_url))

    def test__relation_films_people(self):
        """Test of FilmsPeopleCollector.__relation_films_people method."""
        result = self.collector.__relation_films_people(self.people_data)
        with open(self.get_file_path('output__relation_films_people.json'), 'r') as file_point:
            output = json.load(file_point, object_pairs_hook=OrderedDict)
        self.assertEqual(output, result)

    @patch('app.data_tools.People.get_data')
    @patch('app.data_tools.Films.get_data')
    def test_combine(self, mock_film_get_data, mock_people_get_data):
        """Test of FilmsPeopleCollector.combine method."""
        with open(self.get_file_path('input__combine__films.json'), 'r') as file_point:
            mock_film_get_data.return_value = json.load(file_point, object_pairs_hook=OrderedDict)
        with open(self.get_file_path('input__combine__people.json'), 'r') as file_point:
            mock_people_get_data.return_value = json.load(file_point, object_pairs_hook=OrderedDict)
        with open(self.get_file_path('output__combine.json'), 'r') as file_point:
            output = json.load(file_point, object_pairs_hook=OrderedDict)
        result = self.collector.combine()
        self.assertEqual(output, result)


if __name__ == '__main__':
    unittest.main()
