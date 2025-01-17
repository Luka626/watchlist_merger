#!/usr/bin/env python

LOGGING = "[Watchlist]"

def log_dataframe(outfile):
    print(f'{LOGGING} Saving csv as \'{outfile}\'')

def log_error(error_code):
    print(LOGGING,f"Error: {error_code}")

