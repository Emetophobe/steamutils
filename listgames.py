#!/usr/bin/env python
# Copyright (C) 2019-2023 Mike Cunningham
# https://github.com/Emetophobe/steamutils/

import os
import re
import sys
import glob
import argparse


class SteamInstall:

    def __init__(self, path):
        # Required steam directories
        self.steam_dir = os.path.abspath(path)
        self.steam_apps = os.path.join(self.steam_dir, 'steamapps')
        self.steam_common = os.path.join(self.steam_apps, 'common')

        if not os.path.isdir(self.steam_apps) or not os.path.isdir(self.steam_common):
            raise ValueError('Invalid steam directory')

        self.load_manifests()

    def list_games(self):
        """ List installed games. """
        return sorted(self.games, key=lambda k: k['name'])

    def filter_games(self, search_text):
        """ Filter installed games by name or appid. """
        matches = []
        for game in self.list_games():  # Get sorted list
            if search_text.lower() in game['name'].lower() or search_text in game['appid']:
                matches.append(game)
        return matches

    def load_manifests(self):
        """ Load the app manifest files. """
        self.manifests = glob.glob(os.path.join(self.steam_apps, 'appmanifest_*.acf'))
        self.games = [self._read_manifest(f) for f in self.manifests]

        if not self.manifests or not self.games:
            raise ValueError('Invalid steam directory (found 0 manifest files)')

    def _read_manifest(self, filename):
        """ Read an app manifest into a dictionary. """
        with open(filename, 'r') as infile:
            manifest = {}
            for line in infile:
                # Extract the key/value pairs
                matches = re.findall(r'"(.*?)"', line)  # find strings inside double quotes
                if len(matches) == 2:                   # require a pair of strings
                    key, value = matches[0], matches[1]
                    manifest[key] = value               # store the key/value pair

            # Store extra info about install path and manifest path
            installdir = os.path.join(self.steam_common, manifest['installdir'])
            manifest['_installpath'] = installdir
            manifest['_manifestpath'] = filename

            return manifest


def print_games(games):
    """ Print condensed list of games. """
    row = '{:<45} {:<10} {}'
    print(row.format('Name', 'App id', 'Install path'))
    for game in games:
        print(row.format(game['name'], game['appid'], game['_installpath']))


def print_detailed_games(games):
    """ Print detailed list of games. """
    for game in games:
        print()
        print('name:', game['name'])
        print('appid:', game['appid'])
        print('install path:', game['_installpath'])
        print('manifest file:', game['_manifestpath'])
        print('size:', format_size(game['SizeOnDisk']))


def print_manifests(games):
    """ Print raw manifest details. """
    for game in games:
        for key, value in game.items():
            if not key.startswith('_'):
                print(f'{key}: {value}')
        print()


def format_size(size):
    """ Format size into a human readable string. """
    size = int(size)
    for suffix in ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB'):
        if size < 1024:
            return '{:.1f}{}'.format(size, suffix)
        size /= 1024
    return '{:1f}YB'.format(size)


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
        steam = SteamInstall(args.steamdir)
    except (ValueError, OSError) as e:
        print('Error:', e, file=sys.stderr)
        return 2

    # Apply optional search filter
    if args.search:
        games = steam.filter_games(args.search)
    else:
        games = steam.list_games()

    # Print results
    if games:
        if args.detail:
            print_detailed_games(games)
        elif args.raw:
            print_manifests(games)
        else:
            print_games(games)
    else:
        print('0 games found.')

    return 0

if __name__ == '__main__':
    sys.exit(main())
