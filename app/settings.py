"""
Here project settings are placed.
"""

CACHE_CONFIG = {
    "DEBUG": True,
    "CACHE_TYPE": "memcached",
    "CACHE_DEFAULT_TIMEOUT": 60,
    "CACHE_KEY_PREFIX": "movies_",
    "CACHE_MEMCACHED_SERVERS": ['memcached:11211']
}
