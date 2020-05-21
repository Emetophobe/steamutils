#!/usr/bin/env python
# Copyright 2019-2020 ©  Emetophobe (snapnaw@gmail.com)
# https://github.com/Emetophobe/steamutils/

import os
import re
import sys
import glob
import argparse


def get_games(steamdir):
    """ Retrieve the list of games in steamdir. Uses the manifest files found in steamapps directory. """
    # Check if the steam directory is valid
    steam_apps = os.path.join(os.path.abspath(steamdir), 'steamapps')
    steam_common = os.path.join(steam_apps, 'common')
    if not os.path.isdir(steam_apps) and not os.path.isdir(steam_common):
        raise ValueError(f'Error: Invalid steam directory {steamdir}')

    # Get the list of manifest files from steamapps
    acf_files = glob.glob(os.path.join(steam_apps, 'appmanifest_*.acf'))
    if len(acf_files) < 1:
        raise ValueError(f'Error: Found 0 installed games in {steamdir}')

    # Load the manifest files into a list of dictionaries
    games = []
    for filename in acf_files:
        try:
            # Get the manifest dictionary
            manifest = _read_manifest(filename)

            # Add the full installdir and manifest filename to the dictionary
            manifest['installdir'] = os.path.join(steam_common, manifest['installdir'])
            manifest['manifest'] = filename
        except OSError as e:
            print(f'Failed to read {e.filename} ({e.strerror})')
        else:
            games.append(manifest)

    # Return a sorted list of games
    return sorted(games, key=lambda k: k['name'])


def print_game(game):
    """ Print the game data. """
    print()
    print('name:', game['name'])
    print('appid:', game['appid'])
    print('installdir:', game['installdir'])
    print('manifest:', game['manifest'])
    print('size:', _format_size(game['SizeOnDisk']))


def list_games(games):
    """ Print the list of games. """
    print(f'\n{len(games)} installed games.')
    for game in games:
        print_game(game)


def find_games(games, name):
    """ Find games by name or appid. """
    matches = []
    for game in games:
        if name.lower() in game['name'].lower() or name in game['appid']:
            matches.append(game)

    print(f'Found {len(matches)} matching games.')
    for game in matches:
        print_game(game)


def _read_manifest(filename):
    """ Read a manifest file into a dictionary. """
    with open(filename, 'r') as fp:
        manifest = {}
        for line in fp:
            # Extract the key/value pairs
            matches = re.findall(r'"(.*?)"', line)  # find strings inside double quotes
            if len(matches) == 2:                   # require a pair of strings
                key, value = matches[0], matches[1]
                manifest[key] = value               # store the key/value pair
        return manifest


def _format_size(size):
    """ Format size into a human readable string. """
    size = int(size)
    for suffix in ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB'):
        if size < 1024:
            return f'{size:.1f}{suffix}'
        size /= 1024
    return f'{size:1f}YB'


if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description='List installed games or find a specific game.')
    parser.add_argument('steamdir', help='location of the steam directory', type=str)
    parser.add_argument('-f', '--find', metavar='name', help='search for a specific game or app id', type=str)
    args = parser.parse_args()

    # Get the list of games
    try:
        games = get_games(args.steamdir)
    except (OSError, ValueError) as e:
        sys.exit(e)

    # Find specifc games or list all games
    if args.find:
        find_games(games, args.find)
    else:
        list_games(games)
