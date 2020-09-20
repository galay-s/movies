"""
Initialization of app.
Order of lines is important.
"""

from flask import Flask
from flask_caching import Cache

from app import settings


app = Flask(__name__)
app.config.from_mapping(settings.CACHE_CONFIG)
cache = Cache(app)

from app import urls
