
### listgames.py - List Steam games from the command line
---

Installation:

    $ git clone https://github.com/Emetophobe/steamutils

Requirements:

    * Python 3.6 or later

Usage:

    $ ./listgames.py steamdir

Example:

    $ ./listgames.py c:\\games\\steam

    Name                                          App id     Install path
    Batman: Arkham City GOTY                      200260     c:\games\steam\steamapps\common\Batman Arkham City GOTY
    BioShock                                      7670       c:\games\steam\steamapps\common\Bioshock
    Black Mesa                                    362890     c:\games\steam\steamapps\common\Black Mesa
    Command & Conquer™ Remastered Collection      1213210    c:\games\steam\steamapps\common\CnCRemastered
    Cook, Serve, Delicious!                       247020     c:\games\steam\steamapps\common\CookServeDelicious
    Counter-Strike: Global Offensive              730        c:\games\steam\steamapps\common\Counter-Strike Global Offensive
    DUSK                                          519860     c:\games\steam\steamapps\common\Dusk
    Darkwood                                      274520     c:\games\steam\steamapps\common\Darkwood
    Dead Cells                                    588650     c:\games\steam\steamapps\common\Dead Cells
    Disco Elysium                                 632470     c:\games\steam\steamapps\common\Disco Elysium
    FINAL FANTASY VII                             39140      c:\games\steam\steamapps\common\FINAL FANTASY VII
    Huntdown                                      598550     c:\games\steam\steamapps\common\Huntdown
    Icewind Dale: Enhanced Edition                321800     c:\games\steam\steamapps\common\Icewind Dale Enhanced Edition
    Machinarium                                   40700      c:\games\steam\steamapps\common\Machinarium
    Mark of the Ninja                             214560     c:\games\steam\steamapps\common\mark_of_the_ninja
    Metro: Last Light                             43160      c:\games\steam\steamapps\common\Metro Last Light
    Mini Motorways                                1127500    c:\games\steam\steamapps\common\Mini Motorways
    Nuclear Blaze                                 1662480    c:\games\steam\steamapps\common\NuclearBlaze
    One Finger Death Punch 2                      980300     c:\games\steam\steamapps\common\One Finger Death Punch 2
    Project Zomboid                               108600     c:\games\steam\steamapps\common\ProjectZomboid
    RimWorld                                      294100     c:\games\steam\steamapps\common\RimWorld
    Samorost 1                                    1580970    c:\games\steam\steamapps\common\Samorost 1
    Shadow Tactics: Blades of the Shogun          418240     c:\games\steam\steamapps\common\Shadow Tactics
    Steamworks Common Redistributables            228980     c:\games\steam\steamapps\common\Steamworks Shared
    Streets of Rage 4                             985890     c:\games\steam\steamapps\common\Streets of Rage 4
    Terraria                                      105600     c:\games\steam\steamapps\common\Terraria
    The Last Spell                                1105670    c:\games\steam\steamapps\common\The Last Spell
    Thimbleweed Park                              569860     c:\games\steam\steamapps\common\Thimbleweed Park
    Untitled Goose Game                           837470     c:\games\steam\steamapps\common\Untitled Goose Game


You can also search for specific games by name or app id:

    $ ./listgames.py c:\\games\\steam --search Batman

    Name                                          App id     Install path
    Batman: Arkham City GOTY                      200260     c:\games\steam\steamapps\common\Batman Arkham City GOTY
