import pygame
from pygame.math import Vector2

class Tile(pygame.sprite.Sprite):
    def __init__(self, color, transform, size):
        super().__init__()
        self.color = color
        self.transform = Vector2(transform)
        self.size = Vector2(size)

        self.image = pygame.Surface(self.size)
        self.image.fill(color)

        self.collisions = pygame.sprite.Group()

    @property
    def rect(self):
        return pygame.Rect(self.transform.x, self.transform.y, self.size.x, self.size.y)

    def draw(self, window):
        window.screen.blit(self.image, window.calculate_scroll(self.transform))


class TileMap(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    @property
    def tiles(self):
        return self.sprites()

    def draw(self, window):
        for tile in self.tiles:
            tile.draw(window)

    def collision_test(self, rect):
        collisions = []
        for tile in self.tiles:
            if rect.colliderect(tile):
                collisions.append(tile)
        return collisions

