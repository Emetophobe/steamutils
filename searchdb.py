#!/usr/bin/env python
# Copyright 2019-2020 ©  Emetophobe (snapnaw@gmail.com)
# https://github.com/Emetophobe/steamutils/


import sys
import argparse
import requests
from bs4 import BeautifulSoup


def search_db(game):
    """ Search steamdb.info for the game. """
    # Perform the query using Requests
    dbsearch = f'https://steamdb.info/search/?a=app&q={game}&type=1&category=0'
    r = requests.get(dbsearch, headers={'User-Agent': 'Mozilla 5.0/NT'})
    r.raise_for_status()    # throws a Requests Exception on http error

    # Parse the html using BeautifulSoup
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find('table', {'class': 'table table-bordered table-hover'})
    if not table:
        print('Found 0 results.')
        return

    # Create a dictionary of the results
    results = {}
    for row in table.find_all('tr'):
        column = row.text.strip().split('\n')
        if len(column) == 4 and column[0] != 'AppID' and column[2] != 'Name':
            results[column[2]] = column[0]

    # Print the sorted results
    for name, appid in sorted(results.items()):
        sys.stdout.buffer.write(f'{name} (AppID: {appid})\n'.encode('utf8'))

    sys.stdout.buffer.flush()


if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description='Find a game using the Steam Database (https://steamdb.info/search).')
    parser.add_argument('search', help='find a game by name or app id', type=str)
    args = parser.parse_args()

    # Try the search term using steamdb.info
    try:
        search_db(args.search)
    except Exception as e:
        print('Error: ', e)
