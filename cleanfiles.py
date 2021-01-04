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
                                     epilog='Warning: All file changes are final. USE AT YOUR OWN RISK!')
    parser.add_argument('steamdir', help='location of the steam directory', type=str)
    args = parser.parse_args()

    # Get list of installed games
    games = list_games(args.steamdir)

    # Check for manifest files without a matching installdir
    for game in games:
        if not os.path.exists(game['installdir']):
            delete_manifest(game)

    # Check for installdirs without a matching manifest file
    steam_common = os.path.join(args.steamdir, 'steamapps', 'common')
    for path in os.listdir(steam_common):
        path = os.path.join(steam_common, path)
        if os.path.isdir(path):
            for game in games:
                if path == game['installdir']:
                    break
            else:
                delete_directory(path)


def confirm_delete(message):
    """ Prompt user for a yes/no comfirmation before deleting. """
    return input(message).lower() in ('yes', 'y')


def delete_manifest(game):
    """ Delete a left over manifest file. """
    print('\nThe directory for', game['name'], 'no longer exists:', game['installdir'])
    if confirm_delete('Would you like to delete the left over manifest file? '):
        os.remove(game['manifest'])


def delete_directory(installdir):
    """ Delete a left over installdir. """
    print('\nFound a directory without a matching manifest file:', installdir)
    if confirm_delete('Would you like to delete the left over directory? '):
        shutil.rmtree(installdir)


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError) as e:
        print(e)
    except KeyboardInterrupt:
        pass
