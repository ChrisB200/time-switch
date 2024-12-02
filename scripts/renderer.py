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
        self.display = pygame.display.set_mode(self.resolution / self.scale, flags=pygame.FULLSCREEN | pygame.HWSURFACE | pygame.SCALED)
        self.screen = pygame.Surface(self.resolution / self.scale)

        self.old_scroll = Vector2()
        self.true_scroll = Vector2()
        self.scroll_diff = Vector2()

        self.target = None
        self.is_following = True
        self.pan_strength = 20

    def set_target(self, entity):
        self.target = entity

    @property
    def size(self):
        return Vector2(self.resolution / self.scale)

    @property
    def scroll(self):
        scroll = Vector2(int(self.true_scroll.x), int(self.true_scroll.y))
        self.scroll_diff = scroll - self.true_scroll
        print(self.true_scroll)
        return scroll

    def calculate_scroll(self, transform: Vector2):
        transform = transform.copy()
        return Vector2(transform.x - self.scroll.x, transform.y - self.scroll.y)

    def calculate_scroll_rect(self, rect: pygame.Rect):
        rect = rect.copy()
        rect.x -= self.scroll.x
        rect.y -= self.scroll.y
        return rect

    def follow_target(self):
        self.true_scroll.x += ((self.target.transform.x - self.true_scroll.x) - self.size.x / 2) / self.pan_strength
        self.true_scroll.y += ((self.target.transform.y - self.true_scroll.y) - self.size.y / 2) / self.pan_strength

    def update(self):
        if self.target:
            self.follow_target()

    def draw(self):
        self.display.blit(self.screen, Vector2())
