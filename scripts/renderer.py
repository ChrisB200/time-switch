import pygame
from pygame.math import Vector2


class Window:
    def __init__(self, resolution, scale):
        self.native_resolution = Vector2(resolution) / scale  # Low resolution for rendering
        self.scale = scale  # This is now informational; pygame scales for us with SCALED flag

        self.display = pygame.display.set_mode(self.native_resolution, flags=pygame.FULLSCREEN | pygame.SCALED)
        self.screen = pygame.Surface(self.native_resolution)

        self.true_scroll = Vector2(0, 0)  # Floating-point camera position
        self.target = None
        self.pan_strength = 20

    def set_target(self, entity):
        self.target = entity

    @property
    def size(self):
        return self.native_resolution

    def calculate_scroll(self, position: Vector2):
        # Offset a position relative to the camera
        return position - self.true_scroll

    def calculate_scroll_rect(self, rect: pygame.Rect):
        # Offset a rectangle relative to the camera
        rect = rect.copy()
        rect.x -= self.true_scroll.x
        rect.y -= self.true_scroll.y
        return rect

    def follow_target(self):
        if self.target:
            # Smoothly move the camera towards the target
            self.true_scroll.x += ((self.target.transform.x - self.true_scroll.x) - self.size.x / 2) / self.pan_strength
            self.true_scroll.y += ((self.target.transform.y - self.true_scroll.y) - self.size.y / 2) / self.pan_strength

    def update(self):
        if self.target:
            self.follow_target()

    def draw(self):
        # Pygame handles scaling with SCALED; no manual scaling is needed
        self.display.blit(self.screen, (0, 0))

