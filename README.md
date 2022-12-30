# steamutils

* listgames.py - List installed games or find a specific game by name or app id.
* cleanfiles.py - Clean up left over install dirs and manifest files.
* searchdb.py - Search for games using [steamdb.info](https://steamdb.info/search/) (requires [beautifulsoup](https://pypi.org/project/beautifulsoup4/) and [requests](https://pypi.org/project/requests/)).


Requirements:
    * Python 3.6 or later

Installation:

    git clone https://github.com/Emetophobe/steamutils

Usage:

    ./listgames.py steamdir

Example:

    ./listgames.py c:\\games\\steam
