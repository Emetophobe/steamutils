#!/usr/bin/env python
# Copyright (C) 2019-2020   Emetophobe (snapnaw@gmail.com)
# https://github.com/Emetophobe/steamutils/


import sys
import argparse

from steamparser import SteamParser


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description='List installed games or find a specific game.')
    parser.add_argument('steamdir', help='location of the steam directory', type=str)
    parser.add_argument('-s', '--search', metavar='name', help='search for a specific game or app id', type=str)
    parser.add_argument('-v', '--verbose', help='verbose game details', action='store_true')
    args = parser.parse_args()

    # Get installed games
    try:
        steam = SteamParser(args.steamdir)
        games = steam.games()
    except (OSError, ValueError) as e:
        sys.exit(e)

    # Apply optional search filter
    if args.search is not None:
        matches = []
        for game in games:
            if args.search.lower() in game['name'].lower() or args.search in game['appid']:
                matches.append(game)
        games = matches

    # Print games list
    print('Found {} games in {}{}'.format(len(games), args.steamdir, ':\n' if len(games) > 0 else '.'))
    if len(games) < 1:
        return
    elif args.verbose:
        for game in games:
            print('\nname:', game['name'])
            print('appid:', game['appid'])
            print('installdir:', game['installdir'])
            print('manifest:', game['manifest'])
            print('size:', format_size(game['SizeOnDisk']))
    else:
        format_row = "{:<50} {:<10} {}"
        print(format_row.format("Name", "App Id", "Location"))  # header
        for game in games:
            print(format_row.format(game['name'], game['appid'], game['installdir']))


def format_size(size):
    """ Format install size into a human readable string. """
    size = int(size)
    for suffix in ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB'):
        if size < 1024:
            return '{:.1f}{}'.format(size, suffix)
        size /= 1024
    return '{:1f}YB'.format(size)


if __name__ == '__main__':
    main()
