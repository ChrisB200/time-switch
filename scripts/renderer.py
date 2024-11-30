# Modules
import pygame
from pygame.math import Vector2


class Window:
    """
    A class that manages the drawing of the window. This allows for pixel art to be easily upscaled. This class has 2 cameras. A world camera and a foreground camera. The world camera should be for entities in the world which are affected by scale. The foreground camera should be for elements like the cursor.
    """

    def __init__(self, resolution, scale):
        self.resolution = Vector2(resolution)
        self.scale = scale
        self.display = pygame.display.set_mode(resolution)
        self.screen = pygame.Surface(self.resolution / self.scale)
        self.true_scroll = Vector2()

    @property
    def scroll(self):
        self.scroll = Vector2(int(self.true_scroll.x), int(self.true_scroll.y))

    def draw(self):
        self.display.fill((0, 0, 0))
        self.display.blit(pygame.transform.scale(self.screen, self.resolution), (0, 0))
