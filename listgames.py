#!/usr/bin/env python
# Copyright (C) 2019-2022 Mike Cunningham
# https://github.com/Emetophobe/steamutils/

import os
import re
import sys
import glob
import argparse


def list_games(path):
    """ Get list of installed steam games. """
    path = os.path.abspath(path)
    apps = os.path.join(path, 'steamapps')
    common = os.path.join(apps, 'common')

    # Make sure the directories exist
    if not os.path.isdir(apps) or not os.path.isdir(common):
        raise ValueError('Invalid steam directory')

    # Get list of app manifests
    manifests = glob.glob(os.path.join(apps, 'appmanifest_*.acf'))

    # Parse manifest files into a list of dictionaries
    games = [_read_manifest(common, f) for f in manifests]

    # Make sure we have game manifests
    if not manifests or not games:
        raise ValueError('Invalid steam directory (found 0 manifest files)')

    return sorted(games, key=lambda k: k['name'])


def find_games(search, games):
    """ Filter games by name or appid. """
    matches = []
    for game in games:
        if args.search.lower() in game['name'].lower() or args.search in game['appid']:
            matches.append(game)
    return matches


def print_games(games):
    row = '{:<45} {:<10} {}'
    print(row.format('Name', 'App id', 'Install path'))
    for game in games:
        print(row.format(game['name'], game['appid'], game['_installpath']))


def print_detailed_games(games):
    for game in games:
        print()
        print('name:', game['name'])
        print('appid:', game['appid'])
        print('install path:', game['_installpath'])
        print('manifest file:', game['_manifestpath'])
        print('size:', format_size(game['SizeOnDisk']))


def print_manifests(games):
    """ Display the raw manifest details """
    for game in games:
        for key, value in game.items():
            print(key, value)
        print()


def format_size(size):
    """ Format size into a human readable string. """
    size = int(size)
    for suffix in ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB'):
        if size < 1024:
            return '{:.1f}{}'.format(size, suffix)
        size /= 1024
    return '{:1f}YB'.format(size)


def _read_manifest(steam_common, manifest):
    """ Read manifest file into a dictionary. """
    with open(manifest, 'r') as infile:
        data = {}
        for line in infile:
            # Extract the key/value pairs
            matches = re.findall(r'"(.*?)"', line)  # find strings inside double quotes
            if len(matches) == 2:                   # require a pair of strings
                key, value = matches[0], matches[1]
                manifest[key] = value               # store the key/value pair

        # Add install path and manifest path
        data['installpath'] = os.path.join(steam_common, manifest['installdir'])
        data['manifestpath'] = filename
    return data


def main():
    parser = argparse.ArgumentParser(description='List installed games or find a specific game.')
    parser.add_argument('steamdir', help='steam directory')
    parser.add_argument('-s', '--search', help='filter games by name or appid')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-d', '--detail', help='print more details', action='store_true')
    group.add_argument('-r', '--raw', help='print raw manifest data', action='store_true')

    args = parser.parse_args()

    # Get list of installed games
    try:
        games = list_games(args.steamdir)
    except (ValueError, OSError) as e:
        print('Error:', e, file=sys.stderr)
        return 1

    # Apply optional search filter
    if args.search:
        games = find_games(args.search, games)

    # Print results
    if games:
        if args.detail:
            print_detailed_games(games)
        elif args.raw:
            print_raw_games(games)
        else:
            print_games(games)
    else:
        print('0 games found.')

    return 1

if __name__ == '__main__':
    sys.exit(main())
