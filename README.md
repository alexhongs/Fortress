# Fortress
A tank game with curved terrains, dynamic explosions, and some of my original artwork. 

Defeat the AI opponent by moving up and down curved terrain, and aim to shoot. Shoot near the enemy, it will destroy the enemy's ground.

Reproduced an existing game Fortress II RED by Cosmos Entertainment. 

https://youtu.be/q4EUqPmK18s

## Instruction
To get started, download required files mentioned in `Requirements` and run
`main.py`

## Curved Terrain
Using predefined points on map, you can move along the segment between points. When shot bullet touches near the point, it creates more points along the destruction area.

## Original Artwork
Intuitive user interface and dynamic game experience
`Source/Tanks/CannonBullet1.png, Source/Maps/nightpoints.txt, Source/Maps/skypoints.txt, Source/Interface.png, Source/Interface1.png, Source/Emblem/Fire0.png, Source/Emblem/Fire1.png`

## Modified from Original game
Improved artwork from the original game.

`src/Emblem/CurrentPlayerIcon.png, src/Emblem/lostpic.jpg, src/Emblem/mImage.png, src/Emblem/sImage.png, src/Emblem/wonPic.jpg, src/Emblem/helpScreen.png, src/Map/skyT.gif, src/Map/nightT.gif, src/Map/CannonTank1.gif, src/Map/MissileTank1.gif
Original: Cosmos Entertainment <http://fortress2.x2game.com/view/data/pansite.asp>`

`Source/Map/skyB.jpg
Original: <http://wallpapershacker.com/mountains_clouds_castles_flying_moon_art_hd-wallpaper-
1312961/>`

`Source/Emblem/intropage.jpg
Original: <http://game.donga.com/images/gamegru_news/newsimage2/fortress20040504.jpg>`

## Used Directly from Original game
`Source/Tanks/CannonTank.gif
Source/Tanks/MissileTank.gif
Original: Cosmos Entertainment http://fortress2.x2game.com/view/data/pansite.asp`

## Requirements
Version: 4/28/2016

System Requirement: 
- Run on Windows OS
- Python 3.4.4
- Pillow 3.0.0 Python Imaging Library(Fork), Can be downloaded from https://pypi.python.org/pypi/Pillow/3.0.0
