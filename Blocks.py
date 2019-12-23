import random
import time

from Settings import *

vec = pygame.math.Vector2


class Block(object):
    __slots__ = ('x', 'y', 'size', 'blockType')

    def __init__(self, x=0, y=0, size=1, blockType="empty"):
        self.x = x
        self.y = y
        self.size = size
        self.blockType = blockType


class BlockSet(Block):
    # __slots__ = (
    #     'x', 'y', 'size', 'blockType', 'image', 'rect', 'pos', 'f', 'g', 'h', 'neighbors', 'neighboringWalls',
    #     'previous',
    #     'visited', 'direction')

    def __init__(self, x=0, y=0, size=1, blockType="empty"):
        Block.__init__(self, x, y, size, blockType)

        self.pos = vec(int(x / mapDict["GRID_SIZE"]), int(y / mapDict["GRID_SIZE"]))

        self.f = 0
        self.g = 0
        self.h = 0

        self.neighbors = None
        self.neighboringWalls = None

        self.previous = None

        self.imageIndex = 0
        self.t1 = time.time()

        self.done = False

        self.rect = pygame.rect.Rect(self.x, self.y, mapDict["GRID_SIZE"] * self.size,
                                     mapDict["GRID_SIZE"] * self.size)

        if self.blockType == "empty":
            self.image = pygame.Surface((mapDict["GRID_SIZE"] * self.size, mapDict["GRID_SIZE"] * self.size)).convert()
        elif self.blockType == "animation":
            self.images = None
            self.image = None
            self.indexMax = None
        elif self.blockType == "point":
            self.indexMax = len(pointimages) - 1
            self.image = pointimages[0]
            self.images = pointimages
        elif self.blockType == "block":
            self.indexMax = len(blockimages) - 1
            roll = random.randint(0, 100) % len(blockimages)
            self.image = blockimages[roll]
        elif self.blockType == "invincible":
            self.image = pygame.Surface((mapDict["GRID_SIZE"] * self.size, mapDict["GRID_SIZE"] * self.size)).convert()
            self.image.fill((30, 30, 30))

    def update(self):
        if self.blockType == "point":
            self.animate(0.3)
        elif self.blockType == "animation":
            if not self.done:
                self.animate2(0.05)

    def animate2(self, freqency=0.5):
        if (time.time() - self.t1) > freqency and not self.imageIndex > self.indexMax:
            self.image = self.images[self.imageIndex]
            self.imageIndex += 1
            self.t1 = time.time()
        if self.imageIndex > self.indexMax:
            self.done = True

    def animate(self, freqency=0.5):
        if (time.time() - self.t1) > freqency and not self.imageIndex > self.indexMax:
            self.image = self.images[self.imageIndex]
            self.imageIndex += 1
            if self.imageIndex > self.indexMax:
                self.imageIndex = 0
                pass
            self.t1 = time.time()

    def getNeighbors(self, gameobj):
        if not self.neighbors:
            self.populateNeighbors(gameobj)
        return self.neighbors

    def getNeighboringWalls(self, gameobj):
        if not self.neighboringWalls:
            self.populateNeighbors(gameobj)
        return self.neighboringWalls

    def clearNeighbors(self):
        self.neighbors = None
        self.neighboringWalls = None
        self.f = 0
        self.g = 0
        self.h = 0

    def populateNeighbors(self, gameobj):
        self.neighbors = []
        self.neighboringWalls = []

        for i in range(4):
            if i == 0:
                tempy = int(self.pos.y) + 1
                tempx = int(self.pos.x)
                if tempy >= len(gameobj.poslist):
                    tempy = len(gameobj.poslist) - 1
                elif tempy < 0:
                    tempy = 0
                if tempx >= len(gameobj.poslist[tempy]):
                    tempx = len(gameobj.poslist[tempy]) - 1
                elif tempx < 0:
                    tempx = 0
                ind = gameobj.poslist[tempy][tempx]
            elif i == 1:
                tempy = int(self.pos.y) - 1
                tempx = int(self.pos.x)
                if tempy >= len(gameobj.poslist):
                    tempy = len(gameobj.poslist) - 1
                elif tempy < 0:
                    tempy = 0
                if tempx >= len(gameobj.poslist[tempy]):
                    tempx = len(gameobj.poslist[tempy]) - 1
                elif tempx < 0:
                    tempx = 0
                ind = gameobj.poslist[tempy][tempx]
            if i == 2:
                tempy = int(self.pos.y)
                tempx = int(self.pos.x) + 1
                if tempy >= len(gameobj.poslist):
                    tempy = len(gameobj.poslist) - 1
                elif tempy < 0:
                    tempy = 0
                if tempx >= len(gameobj.poslist[tempy]):
                    tempx = len(gameobj.poslist[tempy]) - 1
                elif tempx < 0:
                    tempx = 0
                ind = gameobj.poslist[tempy][tempx]
            elif i == 3:
                tempy = int(self.pos.y)
                tempx = int(self.pos.x) - 1
                if tempy >= len(gameobj.poslist):
                    tempy = len(gameobj.poslist) - 1
                elif tempy < 0:
                    tempy = 0
                if tempx >= len(gameobj.poslist[tempy]):
                    tempx = len(gameobj.poslist[tempy]) - 1
                elif tempx < 0:
                    tempx = 0
                ind = gameobj.poslist[tempy][tempx]

            try:
                if gameobj.blocksetlist[ind].blockType == "empty":
                    gameobj.blocksetlist[ind].direction = dir
                    self.neighbors.append(gameobj.blocksetlist[ind])
                elif gameobj.blocksetlist[ind].blockType != "empty":
                    self.neighboringWalls.append(gameobj.blocksetlist[ind])
            except:
                print("out of bounds")
                continue
