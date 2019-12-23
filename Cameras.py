import pygame

from Settings import mapDict


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        try:
            return target.rect.move(self.state.topleft)
        except:
            print(target)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect  # l = left,  t = top
    _, _, w, h = camera  # w = width, h = height
    return pygame.Rect(-l + mapDict["HALF_WIDTH"], -t + mapDict["HALF_HEIGHT"], w, h)
