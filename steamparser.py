#!/usr/bin/env python
# Copyright (C) 2019-2020   Emetophobe (snapnaw@gmail.com)
# https://github.com/Emetophobe/steamutils/


import os
import re
import glob


class SteamParser:
    """ SteamParser for acf files.

    Parses app manifest (*.acf) files found in the 'steam/steamapps' directory and converts
    them into python dicts. Each dict is a simple key/value string pair.

    Available keys include: appid, name, installdir, SizeOnDisk, BytesDownloaded, LastUpdated,
    LastUpdated, LastOwner, BytesToDownload, InstalledDepots, MountedDepots, InstallScripts,
    UserConfig, StateFlags, Universe, AutoUpdateBehavior, AllowOtherDownloadsWhileRunning,
    ScheduledAutoUpdate.
    """

    def __init__(self, steamdir):
        """ Initialize the parser with the specified Steam directory.

        Parameters
        ----------
        steamdir : str
            The steam directory path

        Raises
        ------
        ValueError
            If the steamdir is invalid
        """

        # Make sure the steam directory is valid
        self.steamdir = steamdir
        self.steam_apps = os.path.join(os.path.abspath(steamdir), 'steamapps')
        self.steam_common = os.path.join(self.steam_apps, 'common')
        if not os.path.isdir(self.steam_apps) and not os.path.isdir(self.steam_common):
            raise ValueError('Error: Invalid steam directory.')

        # Get the list of manifest files from the steamapps directory
        self.acf_files = glob.glob(os.path.join(self.steam_apps, 'appmanifest_*.acf'))
        if len(self.acf_files) < 1:
            raise ValueError('Error: Invalid steam directory (found 0 games).')

    def games(self):
        """ Read the manifest files and creates a list of dicts.

        Raises:
        -------
        OSError
            If a manifest file can't be read
        """
        # Convert acf files into list of game manifests
        games = []
        for filename in self.acf_files:
            try:
                with open(filename, 'r') as fp:
                    manifest = {}
                    for line in fp:
                        # Extract the key/value pairs
                        matches = re.findall(r'"(.*?)"', line)  # find strings inside double quotes
                        if len(matches) == 2:                   # require a pair of strings
                            key, value = matches[0], matches[1]
                            manifest[key] = value               # store the key/value pair

                # Add the full installdir and manifest location to the dictionary
                manifest['installdir'] = os.path.join(self.steam_common, manifest['installdir'])
                manifest['manifest'] = filename
            except OSError as e:
                print('Failed to read {} ({})'.format(e.filename, e.strerror))
            else:
                games.append(manifest)

        return sorted(games, key=lambda k: k['name'])
