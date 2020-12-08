#!/usr/bin/env python
# Copyright (C) 2019-2020   Emetophobe (snapnaw@gmail.com)
# https://github.com/Emetophobe/steamutils/


import os
import sys
import re
import glob
import argparse


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description='List installed games or find a specific game.')
    parser.add_argument('steamdir', help='location of the steam directory', type=str)
    parser.add_argument('-s', '--search', metavar='name', help='search for a specific game or app id', type=str)
    parser.add_argument('-v', '--verbose', help='verbose game details', action='store_true')
    args = parser.parse_args()

    # Get installed games
    try:
        games = list_games(args.steamdir)
    except (OSError, ValueError) as e:
        sys.exit(e)

    # Apply optional search filter
    if args.search is not None:
        matches = []
        for game in games:
            if args.search.lower() in game['name'].lower() or args.search in game['appid']:
                matches.append(game)
        games = matches

    # Print results
    print('Found {} games in {}{}'.format(len(games), args.steamdir, ':' if len(games) > 0 else '.'))
    if len(games) > 0:
        print_games(games, args.verbose)


def list_games(steamdir):
    """ Get the list of installed Steam games. """
    # Make sure the directory is valid
    steam_apps = os.path.join(os.path.abspath(steamdir), 'steamapps')
    steam_common = os.path.join(steam_apps, 'common')
    if not os.path.isdir(steam_apps) and not os.path.isdir(steam_common):
        raise ValueError('Error: Invalid steam directory.')

    # Get list of manifest files from the steamapps directory
    acf_files = glob.glob(os.path.join(steam_apps, 'appmanifest_*.acf'))

    # Parse manifest files and create a list of game dicts
    games = []
    for filename in acf_files:
        with open(filename, 'r') as fp:
            manifest = {}
            for line in fp:
                # Extract the key/value pairs
                matches = re.findall(r'"(.*?)"', line)  # find strings inside double quotes
                if len(matches) == 2:                   # require a pair of strings
                    key, value = matches[0], matches[1]
                    manifest[key] = value               # store the key/value pair

            # Add the full path to the installdir and manifest file
            manifest['installdir'] = os.path.join(steam_common, manifest['installdir'])
            manifest['manifest'] = filename
            games.append(manifest)

    return sorted(games, key=lambda k: k['name'])


def print_games(games, verbose):
    """ Print list of manifest data. """
    if verbose:
        for game in games:
            print('\nname:', game['name'])
            print('appid:', game['appid'])
            print('installdir:', game['installdir'])
            print('manifest:', game['manifest'])
            print('size:', format_size(game['SizeOnDisk']))
    else:
        format_row = "{:<50} {:<10} {}"
        print()
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
