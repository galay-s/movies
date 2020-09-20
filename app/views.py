"""
This module handle all views.
"""

from flask import render_template
from flask.views import MethodView

from app import cache
from app.data_tools import FilmsPeopleCollector


collector = FilmsPeopleCollector()


class FilmsAPI(MethodView):
    """Class-based view for films"""

    @staticmethod
    @cache.cached()
    def get():
        """View method which is cached."""
        return render_template('index.html', films=collector.combine())
