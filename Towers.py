import math
import time
from Settings import *

vec = pygame.math.Vector2


class BaseTower:
    __slots__ = ('x', 'y', 'size', 'blockType', 'image', 'rect')

    def __init__(self, x, y, size, blockType):
        self.x = x
        self.y = y
        self.size = size
        self.blockType = blockType
        self.image = pygame.Surface((mapDict["GRID_SIZE"] * self.size, mapDict["GRID_SIZE"] * self.size)).convert()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))


class RespawnTower(BaseTower):
    # __slots__ = ('x', 'y', 'size', 'blockType', 'image', 'rect', 'target', 'vision', 'pos')

    def __init__(self, x, y, size, blockType, target):
        BaseTower.__init__(self, x, y, size, blockType)
        self.vision = pygame.rect.Rect(self.x, self.y, mapDict["GRID_SIZE"] ** self.size * 5,
                                       mapDict["GRID_SIZE"] * self.size * 5)
        self.vision.center = (self.x, self.y)
        self.imageIndex = 0
        self.images = respawnimages

        self.image = self.images[self.imageIndex]
        self.pos = vec(int(x / mapDict["GRID_SIZE"]), int(y / mapDict["GRID_SIZE"]))

        self.target = target

        self.indexMax = len(self.images) -1

        self.t1 = time.time()

    def update(self):
        self.animate(0.3)
        atVision = self.vision.colliderect(self.target.rect)
        if atVision:
            self.target.startPos.x = self.x
            self.target.startPos.y = self.y

    def animate(self,  freqency=0.5):

        if (time.time() - self.t1) > freqency:
            self.image = self.images[self.imageIndex]
            self.imageIndex += 1
            if self.imageIndex > self.indexMax:
                self.imageIndex = 0
            self.t1 = time.time()


class Tower(BaseTower):
    # __slots__ = (
    # 'x', 'y', 'size', 'blockType', 'image', 'rect', 'target', 'vision', 'rof', 'rofMax', 'range', 'pos', 'orig_img')

    def __init__(self, x, y, size, blockType, target, range=globDict["vrange"]):
        BaseTower.__init__(self, x, y, size, blockType)
        self.range = range
        self.vision = pygame.rect.Rect(self.x, self.y, mapDict["GRID_SIZE"] * self.range,
                                       mapDict["GRID_SIZE"] * self.range)
        self.images = toweroffimages
        self.image = self.images[0]
        self.vision.center = (self.x, self.y)
        self.pos = vec(int(x / mapDict["GRID_SIZE"]), int(y / mapDict["GRID_SIZE"]))

        self.target = target
        self.rof = 0
        self.rofMax = int((1 / globDict["rof"]) * 1000)

    def update(self):
        atVision = self.vision.colliderect(self.target.rect)
        inVision = self.vision.contains(self.target.rect)

        if atVision or inVision:
            self.images = toweronimages
            self.image = self.images[0]
        else:
            self.images = toweroffimages
            self.image = self.images[0]

        if globDict["collisionON"]:
            self.rof += 1
            if atVision and self.rof % self.rofMax == 0 or inVision and self.rof % self.rofMax == 0:
                bullet = Projectile(self.rect.centerx, self.rect.centery, self.target.rect.centerx,
                                    self.target.rect.centery, 6, "tower")
                self.target.bulletList.append(bullet)
                self.rof = 0


class Projectile:
    __slots__ = (
        'x', 'y', 'tarx', 'tary', 'image', 'rect', 'speed', 'fromwho', 'pos', 'epos', 'd', 'rel_x', 'rel_y', 'run',
        'rise',
        'dist')

    def __init__(self, x, y, tarx, tary, speed, fromwho):
        self.speed = speed
        self.fromwho = fromwho
        self.image = shotImage
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = vec(x, y)

        self.epos = vec(tarx, tary)

        self.rel_x = self.epos.x - self.pos.x
        self.rel_y = self.epos.y - self.pos.y

        self.d = math.hypot(self.rel_x, self.rel_y)

        self.rise = math.sin(self.rel_y / self.d)
        self.run = math.sin(self.rel_x / self.d)

        self.dist = 0

    def update(self, seconds):
        self.pos.x += self.run * self.speed * (seconds * 100)
        self.pos.y += self.rise * self.speed * (seconds * 100)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        self.dist += ((self.run * self.speed) ** 2 + (self.rise * self.speed) ** 2) ** 0.5

        if self.dist > 800:
            return True
