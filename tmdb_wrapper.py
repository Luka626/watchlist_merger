#!/usr/bin/env python

from pathlib import Path
import requests
from logger import log_error

_API_KEY = (Path(__file__).parent / "keys.txt").open().readline().rstrip()
_DOMAIN = "https://api.themoviedb.org/3"
_HEADERS = {
            "accept": "application/json",
            "Authorization": f"Bearer {_API_KEY}"
}

def search_movie(name, release_year, base_url, headers):
    params = {
        "query": name,
        "year": release_year
    }

    response = requests.get(f'{base_url}/search/movie', headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        log_error(response.status_code)
        return None


def fetch_providers(movie_id, base_url, headers):

    response = requests.get(f'{base_url}/movie/{movie_id}/watch/providers', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        log_error(response.status_code)
        return None

def identify_streamer(name, year):
    search_result = search_movie(name, year, _DOMAIN, _HEADERS)

    if search_result is None:
        return None

    movie_id = search_result["results"][0]["id"]
    provider_results = fetch_providers(movie_id, _DOMAIN, _HEADERS)

    if provider_results is None:
        return None

    if "CA" not in provider_results["results"]:
        return None

    if "flatrate" not in provider_results["results"]["CA"]:
        return None

    return provider_results["results"]["CA"]["flatrate"][0]["provider_name"]


