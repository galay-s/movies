"""
Here urls are placed
"""

from app import app
from app.views import FilmsAPI

app.add_url_rule('/movies/', view_func=FilmsAPI.as_view('movies'))
