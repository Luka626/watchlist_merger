#!/usr/bin/env python

from bs4 import BeautifulSoup, NavigableString
import requests
import numpy as np

from logger import log_error

_DOMAIN = 'https://letterboxd.com/'

def scrape_watchlist(user):
    watchlist_url = _DOMAIN + user + "/watchlist/"
    watchlist = []

    while True:
        page_films, page_soup = scrape_page(watchlist_url)
        if not page_films or not page_soup:
            return watchlist

        watchlist.extend(page_films)

        next = page_soup.find('a', class_='next')

        if next is None or isinstance(next, NavigableString):
            return watchlist

        link = next.get("href")
        if not isinstance(link, str):
            return watchlist

        watchlist_url = _DOMAIN + link

def scrape_page(url):
    page_films = []
    page_response = requests.get(url)
    if page_response.status_code != 200:
        log_error(page_response.status_code)
        return None, None

    page_soup = BeautifulSoup(page_response.content, "lxml")

    table = page_soup.find('ul', class_='poster-list')
    if table is None or isinstance(table, NavigableString):
        return None, None

    films = table.find_all('li')
    if not films:
        return None, None

    for film in films:
        film_data = scrape_film(film)
        page_films.append(film_data)

    return page_films, page_soup

def scrape_film(film_html):
    film_data = {}
    film_card = film_html.find('div').get('data-target-link')[1:]
    film_url = _DOMAIN + film_card
    film_request = requests.get(film_url)
    film_soup = BeautifulSoup(film_request.content, 'html.parser')

    main_content = film_soup.find("div", {"class" : "col-17"})
    if not main_content:
        return None

    title = main_content.find("h1")
    if not title or isinstance(title, int):
        return None

    film_data["Name"] = title.text

    try:
        release_years = film_soup.find_all('div', class_='releaseyear')
        if len(release_years) > 1:  # Check if we have enough elements
            year_text = release_years[1].find('a').text.strip()
            release_year = int(year_text) if year_text else 0
        else:
            release_year = 0
    except (AttributeError, IndexError, ValueError):
        release_year = 0
    film_data["Year"] = np.nan if release_year == 0 else release_year
    film_data["Letterboxd URI"] = film_url
    return film_data

