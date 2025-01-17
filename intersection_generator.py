#!/usr/bin/env python

import pandas as pd
import os

import logger
from tmdb_wrapper import identify_streamer
from scraper import scrape_watchlist
    
class IntersectionGenerator:
    def __init__(self, users, outfile):
        self.users = users
        self.outfile = outfile
        self.dataframes = self.fetch_dataframes()

    def fetch_dataframes(self):
        dataframes = []
        for user in self.users:
            path = user + "/watchlist.csv"
            if (os.path.exists(path)):
                df = pd.read_csv(f'{user}/watchlist.csv')
            else:
                scrape = scrape_watchlist(user)
                df = pd.DataFrame(scrape)
            dataframes.append(df)
            print(f'{logger.LOGGING} {user}\'s watchlist length: {df["Name"].count()}')
        return dataframes

    def generate_intersection(self):
        intersection = pd.DataFrame()

        for df in self.dataframes:
            if intersection.empty:
                intersection = df
            else:
                intersection = pd.merge(intersection, df, on=["Name", "Year", "Letterboxd URI"])
                intersection = intersection.drop(["Date_x", "Date_y"], axis=1, errors="ignore")

        intersection_watchlist = intersection.drop("Letterboxd URI", axis=1)
        intersection_watchlist.to_csv(self.outfile, encoding="utf-8", index=False, header=True)
        logger.log_dataframe(self.outfile)

    def query_providers(self):
        intersection_df = pd.read_csv(self.outfile)

        print(logger.LOGGING,f'Watchlists contain {intersection_df["Name"].count()} common items:')
        print(logger.LOGGING,"Fetching streaming providers...")

        intersection_dict = intersection_df.to_dict('index')
        providers = []
        for _, movie in intersection_dict.items():
            name = movie["Name"]
            year = movie["Year"]

            provider = identify_streamer(name, year)
            if provider is None:
                provider = "N/A"
            providers.append(provider)

        intersection_df["Provider"] = providers
        intersection_df.to_csv(self.outfile, encoding="utf-8", index=False, header=True)
        logger.log_dataframe(self.outfile)
