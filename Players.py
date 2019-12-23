import pygame
import math

from Misc import removeBlock, Animation
from Settings import mapDict, globDict, explimages
from Settings import shipImage
from Towers import Projectile

vec = pygame.math.Vector2


class Player:
    def __init__(self):
        self.image = shipImage
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.rect.height -= 2
        self.rect.width -= 2

        self.rectLeft = pygame.rect.Rect(self.rect.x - 3, self.rect.y + 1, 3, self.rect.height * 0.8)
        self.rectRight = pygame.rect.Rect(self.rect.x + self.rect.width, self.rect.y + 1, 3, self.rect.height * 0.8)
        self.rectUp = pygame.rect.Rect(self.rect.x + 1, self.rect.y - 3, self.rect.width * 0.8, 3)
        self.rectDown = pygame.rect.Rect(self.rect.x + 1, self.rect.y + self.rect.height, self.rect.width * 0.8, 3)

        self.rectOuter = pygame.rect.Rect(self.rect.x - 6, self.rect.y - 6, self.rect.width + 14, self.rect.height + 14)

        self.blockType = "player"
        self.startPos = vec(0, 0)
        self.pos = vec(0, 0)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.orig_img = self.image

        self.rotation = 90

        self.PLAYER_FRICTIONX = -0.02
        self.PLAYER_FRICTIONY = -0.02
        self.PLAYER_ACC = mapDict["GRID_SIZE"]
        self.gravity = 0
        self.onGround = False

        self.jumpcount = 0

        self.hitright = False
        self.hitleft = False
        self.hitup = False
        self.hitdown = False

        self.health = 100

        self.bulletList = []
        self.rof = 9

        self.resetting = False

    def heal(self):
        self.health += 1

        if self.health > 100:
            self.health = 100

    def hit(self):
        self.health -= 1

        if self.health <= 0:
            self.resetting = True
            self.reset()

    def reset(self):
        self.health = 100
        self.pos = vec(self.startPos.x, self.startPos.y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.resetting = False

    def rotate(self, mousex=0, mousey=0, angle=0):
        if angle == 0:
            mouse_pos = vec(mousex, mousey)
            rel_x, rel_y = mouse_pos - self.pos
            angle = -(math.degrees(math.atan2(rel_y, rel_x)) + 90)
            self.rotation += angle
        self.image = pygame.transform.rotate(self.orig_img, angle)

    def update(self, gameobj, seconds):

        self.rof += 1

        if gameobj.keystate[14] and self.rof % 30 == 0:
            tempx, tempy = pygame.mouse.get_pos()
            mousex = (tempx + self.pos.x) - mapDict["HALF_WIDTH"] - 7
            mousey = (tempy + self.pos.y) - mapDict["HALF_HEIGHT"] - 7
            self.rotate(mousex, mousey)
            bullet = Projectile(self.rect.centerx, self.rect.centery, mousex, mousey, 20, "player")
            self.bulletList.append(bullet)
            self.rof = 0

        for bult in self.bulletList:
            if bult.update(seconds):
                self.bulletList.remove(bult)
                break
            if bult.fromwho == "tower" and bult.rect.colliderect(self.rect):
                self.hit()
                self.bulletList.remove(bult)
                break
            if bult.fromwho == "player":
                entcollist = bult.rect.collidelistall(gameobj.entlist)
                for e in entcollist:
                    gameobj.entlist.pop(e)
                    self.bulletList.remove(bult)
                    break

            for col in (bult.rect.collidelistall(gameobj.drawrect)):
                px = int(gameobj.drawlist[col].x / mapDict["GRID_SIZE"])
                py = int(gameobj.drawlist[col].y / mapDict["GRID_SIZE"])
                ind = gameobj.poslist[py][px]
                if (gameobj.blocksetlist[ind].blockType == "tower" and bult.fromwho != "tower") or gameobj.blocksetlist[
                   ind].blockType == "block":
                    removeBlock(gameobj, px, py)
                    Animation(gameobj, px, py, explimages)
                    self.bulletList.remove(bult)
                    break
                elif gameobj.blocksetlist[ind].blockType in ("respawntower", "invincible", "end"):
                    self.bulletList.remove(bult)
                    break

        if not self.resetting:
            self.acc = vec(0, 0)
            if gameobj.keystate[0] and not self.hitright:
                self.acc.x = self.PLAYER_ACC * seconds
                self.rotate(angle=-(90 - self.rotation))
                self.rotation = 0
            if gameobj.keystate[1] and not self.hitleft:
                self.acc.x = -self.PLAYER_ACC * seconds
                self.rotate(angle=(90 - self.rotation))
                self.rotation = 0
            if gameobj.keystate[2] and not self.hitdown and not gameobj.keystate[5]:
                self.acc.y = self.PLAYER_ACC * seconds
                self.rotate(angle=-(90 - self.rotation))
                self.rotation = -90
            if gameobj.keystate[3] and not self.hitup and not gameobj.keystate[5]:
                self.acc.y = -self.PLAYER_ACC * seconds
                self.rotate(angle=(-1))
                self.rotation = -1

            self.acc.x += self.vel.x * self.PLAYER_FRICTIONX
            self.acc.y += self.vel.y * self.PLAYER_FRICTIONY
            self.acc.y = self.acc.y + self.gravity

            self.vel += self.acc

            gameobj.player.pos += self.vel + mapDict["GRID_SIZE"] * seconds * self.acc

            self.rect.topleft = self.pos
            self.rectLeft.topleft = (self.rect.x - 3, self.rect.y + 3)
            self.rectRight.topleft = (self.rect.x + self.rect.width, self.rect.y + 3)
            self.rectUp.topleft = (self.rect.x + 3, self.rect.y - 3)
            self.rectDown.topleft = (self.rect.x + 3, self.rect.y + self.rect.height)

            self.rectOuter.topleft = (self.rect.x - 6, self.rect.y - 6)

        if globDict["collisionON"]:

            if not self.onGround:
                self.PLAYER_FRICTIONY = -0.02
                if gameobj.keystate[5]:
                    self.gravity = (self.PLAYER_ACC * seconds)
                else:
                    self.gravity = 0
            elif self.onGround:
                self.gravity = 0

            for col in (self.rectOuter.collidelistall(gameobj.drawrect)):
                if gameobj.drawlist[col].blockType == "point":
                    gameobj.drawrect.remove(gameobj.drawlist[col])
                    px = int(gameobj.drawlist[col].x / mapDict["GRID_SIZE"])
                    py = int(gameobj.drawlist[col].y / mapDict["GRID_SIZE"])
                    removeBlock(gameobj, px, py)

            if self.rectLeft.collidelistall(gameobj.drawrect) or gameobj.player.pos.x < 0:
                self.hitleft = True
                self.vel.x = 0
                self.acc.x = 0
                # print("Left side hit")
            else:
                self.hitleft = False
            if self.rectRight.collidelistall(gameobj.drawrect) or gameobj.player.pos.x > mapDict["MAP_WIDTH"] - 48:
                self.hitright = True
                self.vel.x = 0
                self.acc.x = 0
                # print("Right side hit")
            else:
                self.hitright = False

            if self.rectUp.collidelistall(gameobj.drawrect) or gameobj.player.pos.y < 0:
                self.hitup = True
                self.vel.y = 0
                self.acc.y = 0
                # print("Top side hit")
            else:
                self.hitup = False
            if self.rectDown.collidelistall(gameobj.drawrect) or gameobj.player.pos.y > mapDict["MAP_HEIGHT"] - 48:
                self.hitdown = True
                self.vel.y = 0
                self.acc.y = 0
                self.onGround = True
                # print("Bot side hit")
            else:
                self.onGround = False
                self.hitdown = False

        else:
            if gameobj.keystate[13]:
                for col in (self.rect.collidelistall(gameobj.drawrect)):
                    px = int(gameobj.drawlist[col].x / mapDict["GRID_SIZE"])
                    py = int(gameobj.drawlist[col].y / mapDict["GRID_SIZE"])
                    removeBlock(gameobj, px, py)
        return self.pos

    def jump(self, height, gameobj):
        if gameobj.keystate[5]:
            if self.onGround:
                self.jumpcount = 0
                self.jumpcount += 1
                self.vel.y = -height
            elif not self.onGround:
                if self.jumpcount == 2:
                    pass
                else:
                    self.jumpcount += 1
                    self.vel.y = -height
