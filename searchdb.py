#!/usr/bin/env python
# Copyright (C) 2019-2020   Emetophobe (snapnaw@gmail.com)
# https://github.com/Emetophobe/steamutils/


import sys
import argparse
import requests

from bs4 import BeautifulSoup


if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description='Find a game using the Steam Database (https://steamdb.info/search).')
    parser.add_argument('search', help='find a game by name or app id', type=str)
    args = parser.parse_args()

    # Perform the query using Requests
    try:
        url = 'https://steamdbasd.info/search/?a=app&q={}&type=1&category=0'.format(args.search)
        r = requests.get(url, headers={'User-Agent': 'Mozilla 5.0/NT'})
        r.raise_for_status()    # throws a Requests Exception on http error
    except requests.RequestException as e:
        print(e.strerror)
        sys.exit(0)

    # Parse html response using BeautifulSoup
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find('table', {'class': 'table table-bordered table-hover'})
    if not table:
        print('Found 0 results.')
        sys.exit(0)

    # Create a dict of games and app ids
    results = {}
    for row in table.find_all('tr'):
        column = row.text.strip().split('\n')
        if len(column) == 4 and column[0] != 'AppID' and column[2] != 'Name':
            results[column[2]] = column[0]

    # Print the results
    for name, appid in sorted(results.items()):
        sys.stdout.buffer.write('{} (AppID: {})\n'.format(name, appid).encode('utf8'))
    sys.stdout.buffer.flush()
