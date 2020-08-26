from functools import lru_cache

import requests


@lru_cache(maxsize=2)
def get_session(base_url: str, pool_size: int):
    session = requests.Session()
    session.mount(base_url, requests.adapters.HTTPAdapter(
        pool_connections=pool_size,
        pool_maxsize=pool_size,
    ))
    return session
