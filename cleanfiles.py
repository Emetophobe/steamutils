#!/usr/bin/env python
# Copyright (C) 2019-2020   Emetophobe (snapnaw@gmail.com)
# https://github.com/Emetophobe/steamutils/

import os
import shutil
import argparse
from listgames import get_games


def check_issues(steamdir):
    """ Check for issues with app manifests and game directories. """
    # Get the list of games
    games = get_games(steamdir)
    issues = 0

    # Search for manifests with missing installdirs
    for game in games:
        if not os.path.exists(game['installdir']):
            delete_manifest(game)
            issues = issues + 1

    # Search for directories without a manifest file
    steam_common = os.path.join(steamdir, 'steamapps', 'common')
    for filename in os.listdir(steam_common):
        filename = os.path.join(steam_common, filename)
        if os.path.isdir(filename):
            for game in games:
                if filename == game['installdir']:
                    break
            else:
                delete_directory(filename)
                issues = issues + 1

    if not issues:
        print('Found 0 issues.')


def delete_manifest(game):
    """ Prompt to delete an unused manifest file without a matching game directory. """
    print(f'\nThe directory for {game["name"]} no longer exists: {game["installdir"]}')
    result = input('Would you like to remove the unused manifest file? [Y/N] ').lower()
    if result == 'yes' or result == 'y':
        try:
            os.remove(game['manifest'])
        except OSError as e:
            print(f'Failed to delete: {e.filename} ({e.strerror})')
    else:
        print('Skipping')


def delete_directory(installdir):
    """ Prompt to delete an uninstalled installdir without a matching manifest file. """
    print(f'\nFound a directory without a matching manifest file: {installdir}')
    result = input('Would you like to delete it? [Y/N] ').lower()
    if result == 'yes' or result == 'y':
        try:
            shutil.rmtree(installdir)
        except OSError as e:
            print(f'Failed to delete: {installdir} ({e.strerror})')
    else:
        print('Skipping')


if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description='Clean up left over files and directories.',
                                     epilog='All changes are final. USE AT YOUR OWN RISK!')
    parser.add_argument('steamdir', help='location of the steam directory', type=str)
    args = parser.parse_args()

    # Check for issues
    try:
        check_issues(args.steamdir)
    except (OSError, ValueError) as e:
        print(e)
    except KeyboardInterrupt:
        pass
