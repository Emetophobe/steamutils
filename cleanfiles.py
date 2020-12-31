#!/usr/bin/env python
# Copyright (C) 2019-2020   Emetophobe (snapnaw@gmail.com)
# https://github.com/Emetophobe/steamutils/

import os
import shutil
import argparse

from listgames import list_games


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description='Clean up left over files and directories.',
                                     epilog='All changes are final. USE AT YOUR OWN RISK!')
    parser.add_argument('steamdir', help='location of the steam directory', type=str)
    args = parser.parse_args()

    # Get installed games
    games = list_games(args.steamdir)

    # Search for manifests without a matching installdir
    issues = 0
    for game in games:
        if not os.path.exists(game['installdir']):
            delete_manifest(game)
            issues += 1

    # Search for directories without a matching manifest
    steam_common = os.path.join(args.steamdir, 'steamapps', 'common')
    for filename in os.listdir(steam_common):
        path = os.path.join(steam_common, filename)
        if os.path.isdir(path):
            for game in games:
                if path == game['installdir']:
                    break
            else:
                delete_directory(path)
                issues += 1

    if not issues:
        print('Found 0 issues.')


def delete_manifest(game):
    """ Prompt to delete an unused manifest file without a matching game directory. """
    print('\nThe directory for {} no longer exists: {}'.format(game['name'], game['installdir']))
    result = input('Would you like to remove the unused manifest file? [Y/N] ').lower()
    if result == 'yes' or result == 'y':
        os.remove(game['manifest'])
    else:
        print('Skipping')


def delete_directory(installdir):
    """ Prompt to delete an uninstalled installdir without a matching manifest file. """
    print('\nFound a directory without a matching manifest file: {}'.format(installdir))
    result = input('Would you like to delete it? [Y/N] ').lower()
    if result == 'yes' or result == 'y':
        shutil.rmtree(installdir)
    else:
        print('Skipping')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError) as e:
        print(e)
    except KeyboardInterrupt:
        pass
