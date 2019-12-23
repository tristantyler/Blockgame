import pygame
import random
from Settings import mapDict, globDict, npcImage
from Pathfinding import *
from Towers import Projectile

vec = pygame.math.Vector2


class EmptyNPC:
    def __init__(self, x, y, size, blockType, range, rofMax):
        self.x = x
        self.y = y
        self.size = size
        self.blockType = blockType
        self.range = range
        self.rofMax = rofMax


class NPC:
    def __init__(self, x, y, size, blockType, target, range=globDict["vrange"]):
        self.size = size
        self.pos = vec(x, y)
        self.startX = x
        self.startY = y
        self.blockType = blockType
        self.image = npcImage
        # self.image = pygame.Surface((mapDict["GRID_SIZE"] * self.size, mapDict["GRID_SIZE"] * self.size)).convert()
        # self.image.fill((random_color()))
        self.rect = pygame.rect.Rect(x, y, 20, 20)
        self.range = range
        self.vision = pygame.rect.Rect(x, y, mapDict["GRID_SIZE"] * self.range * 2,
                                       mapDict["GRID_SIZE"] * self.range * 2)
        self.vision.center = (x, y)
        self.target = target

        self.pather = None
        self.pathRes = None
        self.path = None
        self.pathLen = None
        self.currentPath = None
        self.futurePath = None

        self.step = None

        self.look = False

        self.atEdge = False

        self.d = 9999

        self.count = 0
        self.movecount = 0

        self.rof = 0
        self.rofMax = int((1 / globDict["rof"]) * 1000)

    def getTargetPos(self, gameobj):
        self.atEdge = False
        targetX = int(self.target.pos.x / mapDict["GRID_SIZE"])
        if targetX >= mapDict["XMAX_GRID"] - 1:
            targetX = mapDict["XMAX_GRID"] - 1
            self.atEdge = True
        elif targetX < 0:
            targetX = 0
            self.atEdge = True
        targetY = int(self.target.pos.y / mapDict["GRID_SIZE"])
        if targetY >= mapDict["YMAX_GRID"] - 1:
            targetY = mapDict["YMAX_GRID"] - 1
            self.atEdge = True
        elif targetY < 0:
            targetY = 0
            self.atEdge = True

        ind = gameobj.poslist[targetY][targetX]

        return ind

    def getPos(self, gameobj):
        posX = int(self.pos.x / mapDict["GRID_SIZE"])
        posY = int(self.pos.y / mapDict["GRID_SIZE"])

        try:
            ind = gameobj.poslist[posY][posX]
        except:
            print("invalid get pos")
            ind = gameobj.poslist[mapDict["YMAX_GRID"] - 1][mapDict["XMAX_GRID"] - 1]
        return ind

    def setPathFinder(self, gameobj):  # call after npc creation
        tarind = self.getTargetPos(gameobj)
        if gameobj.blocksetlist[tarind].blockType == "empty":
            self.pather = PathFinder(gameobj.blocksetlist[self.getPos(gameobj)], gameobj.blocksetlist[tarind])
            self.outofsight()
            self.look = True

    def update(self, gameobj):
        atVision = self.vision.colliderect(self.target.rect)

        if globDict["collisionON"] and self.d <= (mapDict["GRID_SIZE"] * 5):
            self.calcTargetDist()
            self.rof += 1
            if atVision and self.rof % self.rofMax == 0:
                bullet = Projectile(self.rect.centerx, self.rect.centery, self.target.rect.centerx,
                                    self.target.rect.centery, 6, "tower")
                self.target.bulletList.append(bullet)
                self.rof = 0
                self.outofsight()
        if atVision and not self.look:
            self.setPathFinder(gameobj)
        elif atVision:
            self.calcTargetDist()
            if self.d > (mapDict["GRID_SIZE"] * 5) and not self.atEdge:
                if self.path is None:
                    while self.pathRes is None:
                        self.searchStep(gameobj)
                    if self.pathRes != -1:
                        self.calcPath()
                elif self.pathLen is not None:
                    self.move()
            elif self.atEdge or self.d <= 20:
                self.outofsight()

    def move(self):
        self.count += 1
        if self.count % 15 == 0:
            if self.step == -1:
                self.outofsight()
                return
            elif self.path[self.step] == "left":
                self.pos.x -= mapDict["GRID_SIZE"]
            elif self.path[self.step] == "right":
                self.pos.x += mapDict["GRID_SIZE"]
            elif self.path[self.step] == "up":
                self.pos.y -= mapDict["GRID_SIZE"]
            elif self.path[self.step] == "down":
                self.pos.y += mapDict["GRID_SIZE"]
            self.step -= 1

            self.rect.x = self.pos.x
            self.rect.y = self.pos.y
            self.vision.center = (self.rect.centerx, self.rect.centery)
            self.count = 0

    def searchStep(self, gameobj):
        result = self.pather.step(gameobj)

        if result == 0:
            pass
        elif result == -1:
            print("No PAth")
            self.look = False
            self.pathRes = result
        else:
            self.pathRes = result
            self.currentPath = result

    def calcPath(self):
        self.path = []

        while self.currentPath is not None:
            if self.currentPath.previous is None:
                break
            else:
                self.futurePath = self.currentPath.previous

            curx = self.currentPath.x
            cury = self.currentPath.y
            futx = self.futurePath.x
            futy = self.futurePath.y

            if futx < curx:
                self.path.append("right")
            elif futx > curx:
                self.path.append("left")
            elif futy < cury:
                self.path.append("down")
            elif futy > cury:
                self.path.append("up")

            self.currentPath.previous = None

            self.currentPath = self.futurePath
        self.pathLen = len(self.path) - 1
        self.step = self.pathLen

        self.pather.closedSet.clear()
        self.pather.openSet.clear()

    def calcTargetDist(self):
        epos = vec(self.target.pos.x, self.target.pos.y)
        rel_x = epos.x - self.pos.x
        rel_y = epos.y - self.pos.y
        self.d = math.hypot(rel_x, rel_y)

    def outofsight(self):
        self.pathRes = None
        self.path = None
        self.pathLen = None
        self.step = None
        self.movecount = 0
        self.count = 0
        self.currentPath = None
        self.futurePath = None
        self.look = False


def random_color():
    a = random.randint(0, 255)
    b = random.randint(0, 255)
    c = random.randint(0, 255)
    rgbl = [a, b, c]
    return tuple(rgbl)
