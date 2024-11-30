import pygame
from pygame.math import Vector2

from scripts.framework import collision_test


class Entity:
    def __init__(self, assets, transform, size, tag):
        self.assets = assets
        self.transform = Vector2(transform)
        self.size = Vector2(size)
        self.movement = Vector2()
        self.tag = tag

        self.rotation = 0
        self.flip = False
        self.layer = 1
        self.speed = 1
        self.directions = {"left": False, "right": False, "up": False, "down": False}
        self.collisions = {'bottom': False, 'top': False, 'left': False, 'right': False}

        self.action = ""
        self.a_offset = (0, 0)
        self.set_action("run/down")

    @property
    def rect(self):
        return pygame.Rect(self.transform.x, self.transform.y, self.size.x, self.size.y)

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.assets[self.tag + "/" + self.action].copy()

    def update_animation(self, dt):
        self.animation.update(dt)

    def move(self, movement, tiles, dt):
        # x-axis
        self.transform.x += movement[0] * dt
        self.rect.x = self.transform.x
        tileCollisions = collision_test(self.rect, tiles)
        objectCollisions = {'bottom': False, 'top': False, 'left': False, 'right': False}
        for tile in tileCollisions:
            if movement[0] > 0:
                self.rect.right = tile.left
                objectCollisions["right"] = True
            elif movement[0] < 0:
                self.rect.left = tile.right
                objectCollisions["left"] = True
        self.transform.x = int(self.rect.x)

        # y-axis
        self.transform.y += movement[1] * dt
        self.rect.y = self.transform.y
        tileCollisions = collision_test(self.rect, tiles)
        for tile in tileCollisions:
            if movement[1] > 0:
                self.rect.bottom = tile.top
                objectCollisions["bottom"] = True
            elif movement[1] < 0:
                self.rect.top = tile.bottom
                objectCollisions["top"] = True
        self.transform.y = int(self.rect.y)
        self.collisions = objectCollisions

    def get_center(self):
        x = self.transform.x - (self.width // 2)
        y = self.transform.y - (self.height // 2)
        return Vector2(x, y)

    def draw(self, window):
        img = self.animation.img()
        if self.rotation:
            img = pygame.transform.rotate(img, self.rotation)
        if self.flip:
            img = pygame.transform.flip(img, self.flip, False)
        window.screen.blit(img, self.transform)

