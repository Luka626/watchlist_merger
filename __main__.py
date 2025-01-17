#!/usr/bin/env python

import time
import argparse

from intersection_generator import IntersectionGenerator
from logger import LOGGING

def main():
    start = time.time()

    parser = argparse.ArgumentParser(prog='Watchlist',
                                     description='Takes Letterboxd exports and finds all common films between one or more users\' watchlists, finds where each film is streaming in Canada and saves to .csv',
                                     epilog='Download .zip files of each user\'s Letterboxd data and extract them to a folder in this directory'
                                     )
    parser.add_argument('-u', '--users', nargs='+', help='path to each user\'s data', required=True)
    parser.add_argument('-o', '--output', type=str, help='output .csv path, defaults to \'intersection_watchlist.csv\'', default='intersection_watchlist.csv',required=False)

    args = parser.parse_args()
    users = args.users
    outfile = args.output

    generator = IntersectionGenerator(users, outfile)
    generator.generate_intersection()
    generator.query_providers()

    end = time.time()
    print(LOGGING,f'Execution time: {1000*(end-start):.0f}ms')

if __name__ == "__main__":
    main()
