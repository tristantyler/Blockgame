import os

import pygame

pygame.init()


class Background:
    image = None

    def __init__(self):
        img = pygame.image.load('resources/space3.jpg').convert_alpha()
        ih = img.get_height()
        iw = img.get_width()
        w = int(mapDict["XMAX_GRID"] * mapDict["GRID_SIZE"])
        h = int(mapDict["YMAX_GRID"] * mapDict["GRID_SIZE"])
        bw = int((w / iw) + 0.9)
        bh = int((h / ih) + 0.9)
        self.image = pygame.Surface((w, h))

        count = 0
        for i in range(bh):
            for j in range(bw):
                count += 1
                self.image.blit(img, (j * iw, i * ih))
        print("Prepared Background Image:", count, "images")
        self.rect = self.image.get_rect(topleft=(0, 0))


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
XMAX_GRID = 100
YMAX_GRID = 100
HALF_WIDTH = SCREEN_WIDTH / 2
HALF_HEIGHT = SCREEN_HEIGHT / 2
GRID_SIZE = 32  # at grid size 30 you get close to 60fps in 1080(64*36=total blocks in view)
MAP_WIDTH = GRID_SIZE * XMAX_GRID
MAP_HEIGHT = GRID_SIZE * YMAX_GRID

mapDict = {"SCREEN_WIDTH": SCREEN_WIDTH,
           "SCREEN_HEIGHT": SCREEN_HEIGHT,
           "HALF_WIDTH": HALF_WIDTH,
           "HALF_HEIGHT": HALF_HEIGHT,
           "XMAX_GRID": XMAX_GRID,
           "YMAX_GRID": YMAX_GRID,
           "GRID_SIZE": GRID_SIZE,
           "MAP_WIDTH": MAP_WIDTH,
           "MAP_HEIGHT": MAP_HEIGHT,
           }

globDict = {"collisionON": False,
            "score": 0,
            "scoregoal": 0,
            "blockbuild": "Block",
            "size": 1,
            "vrange": 30,
            "speed": 1,
            "health": 1000,
            "rof": 30}

# Screen and Background init
flags = pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE
pygame.display.set_caption("Block Game")
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((mapDict["SCREEN_WIDTH"], mapDict["SCREEN_HEIGHT"]))
background = pygame.Surface(screen.get_size())
screen.set_alpha(None)
bg = Background()

# Image init, Font Init, Screen rect
cursorImage = pygame.image.load('resources/curs.png').convert_alpha()
cursorRect = cursorImage.get_rect()
shipImage = pygame.image.load('resources/ship4.png').convert_alpha()

npcImage = pygame.image.load('resources/spaceship.png').convert_alpha()

respawnimages = []
for lvl in os.listdir("resources/respawn/"):
    s = 'resources/respawn/' + lvl
    img = pygame.image.load(s).convert_alpha()
    img = pygame.transform.scale(img, (mapDict["GRID_SIZE"], mapDict["GRID_SIZE"]))
    respawnimages.append(img)

blockimages = []
for lvl in os.listdir("resources/block/"):
    s = 'resources/block/' + lvl
    img = pygame.image.load(s).convert_alpha()
    img = pygame.transform.scale(img, (mapDict["GRID_SIZE"], mapDict["GRID_SIZE"]))
    blockimages.append(img)

toweronimages = []
for lvl in os.listdir("resources/tower/on/"):
    s = 'resources/tower/on/' + lvl
    img = pygame.image.load(s).convert_alpha()
    img = pygame.transform.scale(img, (mapDict["GRID_SIZE"], mapDict["GRID_SIZE"]))
    toweronimages.append(img)

toweroffimages = []
for lvl in os.listdir("resources/tower/off/"):
    s = 'resources/tower/off/' + lvl
    img = pygame.image.load(s).convert_alpha()
    img = pygame.transform.scale(img, (mapDict["GRID_SIZE"], mapDict["GRID_SIZE"]))
    toweroffimages.append(img)

pointimages = []
for lvl in os.listdir("resources/point/"):
    s = 'resources/point/' + lvl
    img = pygame.image.load(s).convert_alpha()
    # img = pygame.transform.scale(img, (mapDict["GRID_SIZE"], mapDict["GRID_SIZE"]))
    pointimages.append(img)

explimages = []
for lvl in os.listdir("resources/explosion/"):
    s = 'resources/explosion/' + lvl
    img = pygame.image.load(s).convert_alpha()
    img = pygame.transform.scale(img, (mapDict["GRID_SIZE"], mapDict["GRID_SIZE"]))
    explimages.append(img)

shotImage = pygame.image.load('resources/shot.png').convert_alpha()


shipImage = pygame.transform.scale(shipImage, (mapDict["GRID_SIZE"], mapDict["GRID_SIZE"]))
npcImage = pygame.transform.scale(npcImage, (mapDict["GRID_SIZE"], mapDict["GRID_SIZE"]))

FONT = pygame.font.Font('resources/KaushanScript-Regular.otf', 18)
screenRect = pygame.rect.Rect(0, 0, mapDict["SCREEN_WIDTH"], mapDict["SCREEN_HEIGHT"])

clock = pygame.time.Clock()
