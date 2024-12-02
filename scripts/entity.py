import pygame
from pygame.math import Vector2, clamp
from dataclasses import dataclass

from scripts.framework import Timer, random_color
from scripts.input import Controller
from scripts.map import Tile, TileMap


@dataclass
class Controls:
    move_left: int
    move_right: int
    jump: int


class Entity(pygame.sprite.Sprite):
    def __init__(self, assets, tag, transform, size):
        super().__init__()

        self.assets = assets
        self.transform = Vector2(transform)
        self.size = Vector2(size)
        self.movement = Vector2()
        self.tag = tag
        self.rect = pygame.Rect(
            self.transform.x, self.transform.y, self.size.x, self.size.y
        )

        self.rotation = 0
        self.flip = False
        self.layer = 1
        self.speed = 100
        self.directions = {"left": False, "right": False, "up": False, "down": False}
        self.collisions = pygame.sprite.Group()

        self.action = ""
        self.a_offset = Vector2()
        self.flipped_a_offset = Vector2()
        self.debug = False
        self.debug_color = random_color()
        self.set_action("idle")

    @property
    def image(self):
        img = self.animation.img()
        if self.rotation:
            img = pygame.transform.rotate(img, self.rotation)
        if self.flip:
            img = pygame.transform.flip(img, self.flip, False)
        img.set_colorkey((0, 0, 0))
        return img

    def set_offset(self, offset, flip=None):
        if flip:
            self.flipped_a_offset = Vector2(offset)
        else:
            self.a_offset = Vector2(offset)

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.assets[self.tag + "/" + self.action].copy()

    def update_animation(self, dt):
        self.animation.update(dt)

    def update(self, dt, *groups):
        self.check_collisions(*groups)

    def get_center(self):
        x = self.transform.x + (self.width // 2)
        y = self.transform.y + (self.height // 2)
        return Vector2(x, y)

    def check_collisions(self, *groups):
        for group in groups:
            for sprite in group.sprites():
                if pygame.sprite.collide_rect(self, sprite):
                    self.collisions.add(sprite)
                    self.handle_collision(sprite)
                else:
                    if self.collisions.has(sprite):
                        self.collisions.remove(sprite)

    def handle_collision(self, sprite):
        pass  # This can be overridden by subclasses

    def draw(self, window):
        offset = self.a_offset if not self.flip else self.flipped_a_offset
        if self.debug:
            pygame.draw.rect(
                window.screen, self.debug_color, window.calculate_scroll_rect(self.rect)
            )
        window.screen.blit(self.image, window.calculate_scroll(self.transform + offset))


class Player(Entity):
    def __init__(self, assets, tag, transform, size, input):
        super().__init__(assets, tag, transform, size)
        self.input = input
        self.collision_dirs = {
            "bottom": False,
            "top": False,
            "left": False,
            "right": False,
        }
        # x-axis
        self.direction = Vector2()
        self.speed = 40
        self.max_speed = 120
        self.friction = 2.2
        # y-axis
        self.air_timer = Timer(0.2)
        self.gravity = 600
        self.jump_speed = -280
        self.max_fall_speed = 500
        self.is_grounded = False

    def event_handler(self, event):
        if isinstance(self.input, Controller):
            self.controller_input(event)
        else:
            self.keyboard_input(event)

    def keyboard_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.input.controls.move_left:
                self.directions["left"] = True
            elif event.key == self.input.controls.move_right:
                self.directions["right"] = True
            if event.key == self.input.controls.jump and self.is_grounded:
                self.movement.y = self.jump_speed
                self.is_grounded = False

        if event.type == pygame.KEYUP:
            if event.key == self.input.controls.move_left:
                self.directions["left"] = False
            if event.key == self.input.controls.move_right:
                self.directions["right"] = False

        # Horizontal movement
        self.direction.x = (
            -1 if self.directions["left"] else 1 if self.directions["right"] else 0
        ) * self.speed

    def move(self, dt, tile_map: TileMap):
        collision_dirs = {"bottom": False, "top": False, "left": False, "right": False}

        # x-axis
        self.transform.x += self.movement.x * dt
        self.rect.x = self.transform.x
        tile_collisions = tile_map.collision_test(self.rect)

        for tile in tile_collisions:
            if self.movement.x > 0:
                self.rect.right = tile.rect.left
                collision_dirs["right"] = True
            elif self.movement.x < 0:
                self.rect.left = tile.rect.right
                collision_dirs["left"] = True

        self.transform.x = self.rect.x

        # y-axis
        self.transform.y += self.movement.y * dt
        self.rect.y = self.transform.y
        tile_collisions = tile_map.collision_test(self.rect)

        for tile in tile_collisions:
            if self.movement.y > 0:
                self.rect.bottom = tile.rect.top
                collision_dirs["bottom"] = True
            if self.movement.y < 0:
                self.rect.top = tile.rect.bottom
                collision_dirs["top"] = True

        self.transform.y = self.rect.y
        self.collision_dirs = collision_dirs

    def handle_collision(self, sprite):
        pass

    def animation_states(self):
        if not self.is_grounded:
            self.set_action("jump")
        elif self.direction.x > 0 or self.direction.x < 0:
            self.set_action("run")
        else:
            self.set_action("idle")

    def get_center(self):
        transform = self.transform.copy()
        transform.x = transform.x + (self.size.x // 2)
        transform.y = transform.y + (self.size.y // 2)
        return transform

    def update(self, dt, tile_map, *groups):
        super().update(dt, *groups)
        self.update_animation(dt)
        self.animation_states()

        # apply acceleration
        acceleration = self.direction.x * self.speed * dt
        self.movement.x += acceleration
        self.movement.x = clamp(self.movement.x, -self.max_speed, self.max_speed)

        # apply friction
        if self.direction.x > 0:
            self.flip = False
        elif self.direction.x < 0:
            self.flip = True
        else:
            if self.movement.x > 0:
                self.movement.x = max(
                    0, self.movement.x - self.friction * dt * self.max_speed
                )
            elif self.movement.x < 0:
                self.movement.x = min(
                    0, self.movement.x + self.friction * dt * self.max_speed
                )

        # handle jumping and falling
        if self.collision_dirs["bottom"]:
            self.movement.y = 0
            self.is_grounded = True
            self.air_timer.restart()
        self.movement.y += self.gravity * dt
        self.movement.y = clamp(
            self.movement.y, -self.max_fall_speed, self.max_fall_speed
        )
        self.air_timer.update(dt)
        if self.air_timer.completed:
            self.is_grounded = False

        self.move(dt, tile_map)
