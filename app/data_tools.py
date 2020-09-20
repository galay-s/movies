"""
This module contains classes for working with data received from Studio Ghibli
"""

from abc import ABC, abstractmethod
from collections import OrderedDict, defaultdict

import requests


class DataBase:
    """Base class for getting json data."""

    URL = None

    def get_data(self):
        """Method for getting ordered data."""
        try:
            data = requests.get(self.URL).json(object_pairs_hook=OrderedDict)
        except Exception:
            data = []
        return data


class People(DataBase):
    """Class for getting information about people."""
    URL = "https://ghibliapi.herokuapp.com/people/"


class Films(DataBase):
    """Class for getting information about films."""
    URL = "https://ghibliapi.herokuapp.com/films/"


class DataCollectorAbstract(ABC):
    """Abstract class for combining data from different source/places."""

    @abstractmethod
    def combine(self):
        """Return combined data."""


class FilmsPeopleCollector(DataCollectorAbstract):
    """Class for combining data from different source/places."""

    def combine(self):
        """Return combined data of films and people."""
        people_data = People().get_data()
        films_data = Films().get_data()
        relation_films_people = self.__relation_films_people(people_data)
        for film in films_data:
            film['people'] = relation_films_people.get(film.get('id'), [])
        return films_data

    def __relation_films_people(self, people_data):
        """
        Return relation between films and people based on people data.

        Data is organized to defaultdict(list) where keys are file_id and values are list of people.

        Example:
        input:
        [
            {  # object#1
                "id": "...",
                "films": ["https://.../films/2baf70d1-42bb-4437-b551-e5fed5a87abe"]
                ...
            },
            {...}  # object#2
        ]

        output: (defaultdict)
        {
            "2baf70d1-42bb-4437-b551-e5fed5a87abe": [<object#1>, ...]
        }

        :param people_data: (list of OrderedDicts) List of info about users gotten from Ghibli
        :return: (defaultdict)
        """
        defaultdict_films_people = defaultdict(list)
        for people in people_data:
            for film_url in people.get('films', []):
                film_id = self.__get_film_id(film_url)
                defaultdict_films_people[film_id].append(people)
        return defaultdict_films_people

    @staticmethod
    def __get_film_id(film_url):
        """
        Return film id based on url.

        Example:
        input: 'https://ghibliapi.herokuapp.com/films/2baf70d1-42bb-4437-b551-e5fed5a87abe'
        output: '2baf70d1-42bb-4437-b551-e5fed5a87abe'

        :param film_url: (string)
        :return file id: (string)
        """
        return film_url.rsplit('/', 1)[-1]
