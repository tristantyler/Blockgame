import GameObject
import pygame
from Settings import screenRect, clock


def loop():
    gameobj = GameObject.GameObject()

    while not gameobj.close:
        gameobj.update()
        gameobj.draw()

        pygame.display.update(screenRect)
        clock.tick()


loop()
